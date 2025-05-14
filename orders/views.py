from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, OrderItem, Coupon
import requests
import json
import datetime
from django.contrib import messages


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart':cart})

class CartAddView(PermissionRequiredMixin, View):
    permission_required = 'orders:add_order'
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')

class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')
    
class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = self.form_class
        return render(request, 'orders/order.html', {'order': order, 'form':form})
    
class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = 'https://api.zarinpal.com/pg/v4/payment/request.json'
ZP_API_VERIFY = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
ZP_API_STARTPAY = 'https://www.zarinpal.com/pg/v4/StartPay/{authority}'
description = 'Your Payment Description'
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order,object.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }

        req_data = {
            'merchant_id': MERCHANT,
            'amount': order.get_total_price(),
            'callback_url': CallbackURL,
            'description': description,
            'metadata': 
                {
                'mobile': request.user.phone_number, 'email': request.user.email
                }}
        
        req_header = {
            'accept': 'application/json',
            'content-type': 'application/json',}
        
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error Code: {e_code} \n Error_message: {e_message}")
        
class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if t_status == 'OK':
            req_header = {
                'accept': 'application/json',
                'content-type': 'application/json'}
            
            req_data = {
            'merchant_id': MERCHANT,
            'amount': order.get_total_price(),
            'authority': t_authority}

            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)

            if len(req.json['errors']) == 0:
                e_code = req.json()['errors']['code']
                if e_code == 100:
                    order.paid = True
                    order.save()
                    return HttpResponse('Transaction success')
                
                elif e_code == 101:
                    return HttpResponse('Transaction submitted')
                
                else:
                    return HttpResponse('Transaction failed')
                
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error Code: {e_code} \n Error_message: {e_message}")
        
        else:
            return HttpResponse('Transaction failed or canceled by user.')
        
class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'This Coupon does not exists', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)
