from flask import *
from database import *
import uuid
customer=Blueprint('customer',__name__)
 

@customer.route('/customerhome',methods=['get','post'])
def customerhome():
	cname=session['cname']
	cid=session['cid']
	print(cname)
	return render_template('customerhome.html',cname=cname)


@customer.route('/customer_view_cargos',methods=['get','post'])
def customer_view_cargos():
	data={}
	cname=session['cname']
	cid=session['cid']
	q="select * from packages"
	res=select(q)
	print(res)
	data['cargo']=res
	if 'submit' in request.form:
		search=request.form['search']+'%'
		q="select * from packages where  packname like '%s'"%(search)
		res=select(q)
		if res:
			data['cargo']=res
		else:
			flash("NO RESULTS FOUND")
			return redirect(url_for('customer.customer_view_cargos'))
	return render_template('customer_view_cargos.html',data=data)

@customer.route('/customer_sendfeedback',methods=['get','post'])
def customer_sendfeedback():
	data={}
	cid=session['cid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	if 'submit' in request.form:
		fb=request.form['fb']
		bid=request.form['bid']
		q="insert into feedback values(NULL,'%s','%s','%s','Pending',NOW())"%(cid,bid,fb)
		res=insert(q)
		return redirect(url_for('customer.customer_sendfeedback'))
	q="select * from feedback inner join branches using(branch_id) where customer_id='%s'"%(cid)	
	res=select(q)
	data['fb']=res
	print(res)
	return render_template('customer_sendfeedback.html',data=data)

@customer.route('/customer_book',methods=['get','post'])
def customer_book():
	pid=request.args['id']
	data={}
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	cid=session['cid']
	q="select * from packages where pack_id='%s'"%(pid)
	res=select(q)
	data['price']=res
	#data['packname']=
	print(res)
	if 'submit' in request.form:
		kg=request.form['kg']
		l=request.form['len']
		width=request.form['width']
		fromb=request.form['fromb']
		to=request.form['to']
		floc=request.form['floc']
		loc=request.form['loc']
		q="select * from bookings order by booking_id desc limit 1"
		res=select(q)
		
		q="insert into bookings values(NULL,'%s',curdate(),'%s','%s','%s','%s','%s','%s','%s','Pending','Pending','0','%s')"%(cid,floc,loc,kg,l,width,fromb,to,pid)
		print(q)
		lid=insert(q)
		flash("booked sucessfully")
		return redirect(url_for('customer.customer_view_bookings'))

	return render_template('customer_book.html',data=data)

@customer.route('/customer_review_andrate',methods=['get','post'])
def customer_review_andrate():
	data={}
	cid=session['cid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select * from review_rating inner join branches using(branch_id) where customer_id='%s'"%(cid)
	res=select(q)
	data['rating']=res
	print(res)
	if 'submit' in request.form:
		bid=request.form['bid']
		rate=request.form['rate']
		review=request.form['review']
		q="select * from review_rating where customer_id='%s' and branch_id='%s'"%(cid,bid)
		res=select(q)
		if res:
			q="update review_rating set rating_point='%s',review_comment='%s',review_date=NOW() where customer_id='%s' and branch_id='%s' "%(rate,review,cid,bid)
			update(q)
			return redirect(url_for('customer.customer_review_andrate'))		
		else:
			print("&&&&&&&&&&&&&&&&&&&&&&&&&")
			q="insert into review_rating values(NULL,'%s','%s','%s','%s',NOW())"%(cid,bid,review,rate)
			res=insert(q)
			return redirect(url_for('customer.customer_review_andrate'))
	# q="select * from feedback inner join branches using(branch_id) where customer_id='%s'"%(cid)	
	# res=select(q)
	# data['fb']=res
	# print(res)
	return render_template('customer_review_andrate.html',data=data)


@customer.route('/customer_view_bookings',methods=['get','post'])
def customer_view_bookings():
	data={}
	cid=session['cid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select * from bookings inner join branches ON(branches.branch_id=bookings.from_branch) where customer_id='%s' order by booking_id desc"%(cid)
	res=select(q)
	data['bookings']=res
	print(res)
	if 'action' in request.args:
		action=request.args['action']
		boid=request.args['boid']	
		amt=request.args['amt']
		
		q="select * from payment where booking_id='%s'"%(boid)
		res=select(q)
		if res:
			flash("ALREADY PAID")
			return redirect(url_for('customer.customer_track_cargo'))
			
		else:
			data['amt']=amt

	else:
		action=None
	if 'pay' in request.form:
		amt=request.args['amt']

		q="insert into payment values(NULL,'%s','%s',NOW())"%(boid,amt)
		insert(q)
		# q="insert into cargo_status values(NULL,'%s','Pending',NOW()"%(boid)
		# insert(q)
		q="update bookings set booking_status='Paid' where booking_id='%s'"%(boid)
		update(q)
		return redirect(url_for('customer.customer_track_cargo'))
		flash("PAYMENT SUCESS")
	if 'action1' in request.args:
		action=request.args['action1']
		boid=request.args['boid']	
		q="update bookings set booking_status='Cancelled' where booking_id='%s'"%(boid)
		update(q)
		flash("Booking Cancelled")
		return redirect(url_for('customer.customer_view_bookings'))

	if 'action2' in request.args:
		action2=request.args['action2']
		boid=request.args['boid']	
		amt=request.args['amt']
		q="update bookings set booking_status='Cancelled' where booking_id='%s'"%(boid)
		update(q)
		flash("Booking Cancelled and amount ₹"+amt +"/- will be refunded in few days")
		return redirect(url_for('customer.customer_view_bookings'))
		

	return render_template('customer_view_bookings.html',data=data)


@customer.route('/customer_track_cargo',methods=['get','post'])
def customer_track_cargo():
	data={}
	cid=session['cid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select * from bookings inner join branches ON(branches.branch_id=bookings.from_branch) inner join payment using(booking_id) where customer_id='%s' and booking_status!='Cancelled' order by branch_id desc"%(cid)
	res=select(q)
	data['bookings']=res
	print(res)
	if 'action' in request.args:
		boid=request.args['boid']
		q="SELECT * FROM `cargo_status` WHERE `booking_id`='%s'"%(boid)
		res=select(q)
		if res:
			data['track']=res
		else:
			data['wait']="wait"

	return render_template('customer_track_cargo.html',data=data)



@customer.route('/customer_view_profile',methods=['get','post'])
def customer_view_profile():
	data={}
	username=session['username']
	print(username)
	q="select * from customers inner join login using(username) where username='%s'"%(username)
	res=select(q)
	print(res)
	data['customer']=res
	if 'submit' in request.form:
		ph=request.form['ph']
		
		email=request.form['email']
		
		# uname=request.form['uname']
		# password=request.form['password']
		# q="update login set username='%s' where username='%s'"%(uname,username)
		# update(q)
		q="update customers set phone='%s',email='%s' where username='%s' "%(ph,email,username)
		update(q)
		
		flash("PROFILE UPDATED")
		return redirect(url_for('customer.customer_view_profile'))
	# if 'action' in request.args:
	# 	q="delete login,customer from customer inner join login using(username) where username='%s'"%(username)
	# 	delete(q)
	# 	flash("ACCOUNT DELETED SUCESSFULLY")
	# 	return redirect(url_for('public.home'))
	return render_template('customer_view_profile.html',data=data)



@customer.route('/customer_change_password',methods=['get','post'])
def customer_change_password():
	uname=session['username']
	data={}
	q="select * from login where username='%s'"%(uname)
	res=select(q)
	print(res)
	data['password']=res[0]['password']
	print(data['password'])

	if 'submit' in request.form:
		opass=request.form['opass']
		cpass=request.form['cpass']
		npass=request.form['npass']
		print(opass)
		if opass==data['password']:
			if cpass==npass:
				print("same")
				q="update login set password='%s' where username='%s'"%(npass,uname)
				update(q)
				flash("UPDATED SUCCESSFULLY")
			else:
				flash("PASSWORD DOES NOT MATCH")
			return redirect(url_for('customer.customer_change_password'))
		else:
			flash("Invalid Current password")
			return redirect(url_for('customer.customer_change_password'))
	return render_template('customer_change_password.html',data=data)
