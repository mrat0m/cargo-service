from flask import *
from public import public
from admin import admin
from branch import branch
from staff import staff
from dboy import dboy
from customer import customer

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
from flask import *



app=Flask(__name__)
app.secret_key="hello"
app.register_blueprint(public)
app.register_blueprint(branch,url_prefix='/branch')
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(staff,url_prefix='/staff')
app.register_blueprint(dboy,url_prefix='/dboy')
app.register_blueprint(customer,url_prefix='/customer')


mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '191322@rajagiricollege.edu.in'
app.config['MAIL_PASSWORD'] = 'clintu2107'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


app.run(debug=True,port=5030)
