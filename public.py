from flask import *
from database import *
import random
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def home():
	
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	data={}
	if 'submit' in request.form:
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'"%(uname,password)
		res=select(q)
		if res:
			session['username']=res[0]['username']
			if res[0]['user_type']=='admin':
				return redirect(url_for('admin.adminhome'))

			if res[0]['user_type']=='resigned':
				flash("YOU ARE RESIGNED")
				return redirect(url_for('public.login'))

			if res[0]['user_type']=='inactive':
				flash("YOU ARE BLOCKED")
				return redirect(url_for('public.login'))
				
			if res[0]['user_type']=='resigned':
				flash("YOU ARE RESIGNED")
				return redirect(url_for('public.login'))

			if res[0]['user_type']=='branch':
				q="select branch_id,branch_name from branches where username='%s'"%(uname)
				res=select(q)
				session['bname']=res[0]['branch_name']
				session['bid']=res[0]['branch_id']
				return redirect(url_for('branch.branchhome'))
			if res[0]['user_type']=='staff':
				q="select * from staffs where username='%s'"%(uname)
				res=select(q)
				print(res)
				session['sid']=res[0]['staff_id']
				session['sname']=res[0]['first_name']+" "+res[0]['last_name']
				return redirect(url_for('staff.staffhome'))
			if res[0]['user_type']=='dboy':
				q="select * from deliveryboys where username='%s'"%(uname)
				res=select(q)
				print(res)
				session['did']=res[0]['boy_id']
				session['dname']=res[0]['first_name']+" "+res[0]['last_name']
				return redirect(url_for('dboy.dboyhome'))
			if res[0]['user_type']=='customer':
				q="select * from customers where username='%s'"%(uname)
				res=select(q)
				print(res)
				session['cid']=res[0]['customer_id']
				session['cname']=res[0]['first_name']+" "+res[0]['last_name']
				return redirect(url_for('customer.customerhome'))
		else:
			data['invalid']="Invalid Login Details"

			
	return render_template('login.html',data=data)

@public.route('/customerreg',methods=['get','post'])
def customerreg():
	data={}
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		ph=request.form['phone']
		email=request.form['email']
		lat=request.form['lat']
		lon=request.form['lon']
		uname=request.form['uname']
		password=request.form['password']
		cpassword=request.form['cpassword']
		if cpassword==password:

			q="select * from login where username='%s'"%(uname)
			res=select(q)
			if res:
				flash('THIS USER NAME  ALREADY TAKEN BY ANOTHER USER')
				return redirect(url_for('public.customerreg'))
			else:
				q="select * from branches where phone='%s' or email='%s'"%(ph,email)
				res1=select(q)
				q="select * from deliveryboys where phone='%s' or email='%s'"%(ph,email)
				res2=select(q)
				q="select * from staffs where phone='%s' or email='%s'"%(ph,email)
				res3=select(q)
				if res1 or res2 or res3:
					flash("ALREADY YOU HAVE AN ACCOUNT")
					return redirect(url_for('public.customerreg'))
				else:
					q="insert into login values('%s','%s','customer')"%(uname,password)
					lid=insert(q)		
					q="insert into customers values(NULL,'%s','%s','%s','%s','%s','%s','%s')"%(uname,fname,lname,ph,email,lat,lon)
					insert(q)
					return redirect(url_for('public.customerreg'))
		else:
			flash("PASSWORD AND CONFIRM PASSWORD DOES NOT MATCH")
	return render_template('customerreg.html',data=data)




@public.route('/public_chanagepassword',methods=['get','post'])
def public_chanagepassword():
	data={}
	if 'submit' in request.form:	
		npass=request.form['uname']
		em=request.form['em']
		q="select email,username from login inner join customers using(username) where username='%s' and email='%s' union select email,username from login inner join staffs using(username) where username='%s' and email='%s' union select email,username from login inner join branches using(username) where username='%s' and email='%s' union select email,username from login inner join deliveryboys using(username) where username='%s' and email='%s'"%(npass,em,npass,em,npass,em,npass,em)
		print(q)
		res=select(q)
		if res:
			session['uname']=res[0]['username']
			email=res[0]['email']
			print(email)
			rd=random.randrange(100000,999999,6)
			# msg=str(rd)
			msg='Hi '+str(npass)+', seems like you forgot your password. Dont Worry we are hear to help you.''\n\n Quick CARGO Password Recovery \n\n OTP for password recovery is '+str(rd) +'.Please do not share your OTP with anyone. \n\nThis is a system generated e-mail and please do not reply.\n\nRegards,\nQuick CARGO'
			data['rd']=rd
			print(rd)
			try:
				gmail = smtplib.SMTP('smtp.gmail.com', 587)
				gmail.ehlo()
				gmail.starttls()
				# gmail.login('jomonml24@gmail.com','jomon240998#')
				gmail.login('191322@rajagiricollege.edu.in','1234')
			except Exception as e:
				print("Couldn't setup email!!"+str(e))

			msg = MIMEText(msg)

			msg['Subject'] = 'OTP FOR PASSWORD RECOVRY Quick CARGO'

			msg['To'] = email

			msg['From'] = '191322@rajagiricollege.edu.in'

			try:
				gmail.send_message(msg)
				print(msg)
				flash("Mail successfully sent to " +email)
				session['rd']=rd
				session['email']=email
				# data['email']=email
				return redirect(url_for('public.setotp'))


			except Exception as e:
				flash("ERROR!!! Couldn't send mail to " +email, str(e))
				return redirect(url_for('public.public_chanagepassword'))
		


			
		else:
			flash("Entered username and e-mail are not matched")
			return redirect(url_for('public.public_chanagepassword'))
			
	
		
	
		
	return render_template('public_chanagepassword.html',data=data)


@public.route('/setotp',methods=['get','post'])
def setotp():
	rd=session['rd']
	uname=session['uname']
	data={}
	data['email']=session['email']
	if "otp" in request.form:
		otp=request.form['otp']
		if int(otp)==int(rd):
			data['chp']=uname
		else:
			flash("Invalid OTP")
			return redirect(url_for('public.setotp'))

	if 'update' in request.form:
		uname=request.form['uname']
		p=request.form['p']
		cp=request.form['cp']
		if p==cp:
			print("+++++++++++")
			q="update login set password='%s' where username='%s'"%(p,uname)
			update(q)
			flash("PASSWORD UPDATED SUCCESSFULLY")
			return redirect(url_for('public.login'))
		else:
			flash("PASSWORD MISMATCH")
			data['chp']=uname


	return render_template('setotp.html',data=data)