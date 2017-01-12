# MailgunMailer
Simple Mailgun GUI to send emails via Mailgun

It is written in Flask with SQLalchemy(MySQL)

Huge thanks for awesome Bootstrap 4 Admin theme to https://github.com/modularcode/modular-admin-html (Gevorg Harutyunyan, Aram Manukyan, David Tigranyan)

**Usage :**  
1) Install inside venv : ``` virtualenv venv ; source venv/bin/activate ``` pip install -r requirements.txt  
2) Rename app/config.py.example to app/config.py. Edit and add db connection information  
3) Run ``` python db_seed.py ``` to create database tables and example data  
4) Run app with your favorite app server, navigate to your hostname and port 8090 (or custom defined on app server) and login as : admin@example.com / admin  

<p align="center">
<img src="https://s30.postimg.org/m1l879kg1/image.jpg"/>
</p>
<p align="center">
<img src="https://s30.postimg.org/pz8hwo79d/image.jpg"/>
</p>
