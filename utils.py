from kavenegar import *



def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('34354549726F316A55457A6A3332664653414A706473706675414B666E706F4E53773256337671775133773D')
        params = { 
            'sender' : '2000660110', 
            'receptor': phone_number, 
            'message' :f'Hi,\nYour Verify Code: {code}' }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
