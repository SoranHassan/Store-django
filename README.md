<h1 align="center">🛒 Store Django</h1>
<p align="center"><em>A powerful e-commerce platform built with Django</em></p>

<h2>📌 Features</h2>
<ul>
    <li><b>User Authentication:</b> Login and register via mobile number with OTP verification</li>
    <li><b>Product Catalog:</b> Browse and filter products efficiently</li>
    <li><b>Admin Panel:</b> Manage users, products, and orders seamlessly</li>
    <li><b>Secure Backend:</b> Optimized with Django for robust performance</li>
</ul>

<h2>🛠 Technologies Used</h2>
<ul>
    <li><b>Backend:</b> Django, requests</li>
    <li><b>Database:</b> SQLite (Django’s default database)</li>
    <li><b>Authentication:</b> OTP verification via external API</li>
    <li><b>Frontend:</b> HTML, CSS</li>
</ul>

<h2>🚀 Installation Guide</h2>

<h3>1️⃣ Clone the Repository</h3>
<pre>
    <code>
git clone https://github.com/SoranHassan/Store-django.git
cd Store-django
    </code>
</pre>

<h3>2️⃣ Set Up a Virtual Environment</h3>
<pre>
    <code>
python -m venv env
source env/bin/activate  <!-- Windows: env\Scripts\activate -->
pip install -r requirements.txt
    </code>
</pre>

<h3>3️⃣ Apply Database Migrations</h3>
<pre>
    <code>
python manage.py migrate
    </code>
</pre>
<p><b>Note:</b> Since this project uses SQLite, migrations will automatically create the database file <code>db.sqlite3</code> in the project directory.</p>

<h3>4️⃣ Run the Server</h3>
<pre>
    <code>
python manage.py runserver
    </code>
</pre>

<h3>5️⃣ Access the Application</h3>
<p>Open the project in your browser:</p>
<pre>
    <code>
http://127.0.0.1:8000/
    </code>
</pre>

<h2>🔗 Contribution</h2>
<p>If you would like to contribute:</p>
<ol>
    <li>Fork the repository</li>
    <li>Create a new branch</li>
    <li>Make your changes</li>
    <li>Submit a pull request</li>
</ol>

<h2>📄 License</h2>
<p>This project is open-source under the MIT License.</p>
