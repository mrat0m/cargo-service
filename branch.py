from database import *
import uuid
from flask import *
branch=Blueprint('branch',__name__)
 

@branch.route('/branchhome',methods=['get','post'])
def branchhome():
	bname=session['bname']
	bid=session['bid']
	print(bname,bid)
	return render_template('branchhome.html',bname=bname)

 
@branch.route('/branch_manage_staffs',methods=['get','post'])
def branch_manage_staffs():
	data={}
	bname=session['bname']
	bid=session['bid']
	data['bid']=bid
	data['bname']=bname
	q="select * from branches"
	data['branch']=select(q)
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		ph=request.form['phone']
		email=request.form['email']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s'"%(uname)
		res=select(q)
		if res:
			flash('THIS USER NAME AND PASSWORD ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('branch.branch_manage_staffs'))
		else:
			q="insert into login values('%s','%s','staff')"%(uname,password)
			lid=insert(q)
			
			q="insert into staffs values(NULL,'%s','%s','%s','%s','%s','%s')"%(uname,fname,lname,bid,ph,email)
			insert(q)
			return redirect(url_for('branch.branch_manage_staffs'))
	q="select * from staffs inner join login using(username) where branch='%s' order by first_name"%(bid)
	res=select(q)
	if res:
		data['staffs']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update login set user_type='staff' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_manage_staffs'))
	if action=='inactive':
		q="update login set user_type='inactive' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_manage_staffs'))
	if action=='resigned':
		print("&&&&&&&&&&")
		
		q="update login set user_type='resigned' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_manage_staffs'))
	if action=='delete':
		q="delete from staffs where staff_id='%s'"%(id)
		delete(q)
		return redirect(url_for('branch.branch_manage_staffs'))
	if action=='update':
		q="select * from staffs where staff_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		ph=request.form['phone']
		email=request.form['email']
		branch=request.form['branch']
		q="update staffs set first_name='%s',last_name='%s',phone='%s',email='%s',branch='%s' where staff_id='%s'"%(fname,lname,ph,email,branch,id)
		update(q)
		if int(branch)!=int(bid):
			flash(fname+" transfer updated")
		else:
			flash("UPDATED SUCCESFULLY")
		return redirect(url_for('branch.branch_manage_staffs'))

	if 'find' in request.form:
		search=request.form['search']+'%'
		q="select * from staffs inner join login using(username) where branch='%s' and first_name like '%s' order by first_name"%(bid,search)
		res=select(q)
		if res:
			data['staffs']=res	
		else:
			flash("NO RESULTS FOUND")
			return redirect(url_for('branch.branch_manage_staffs'))
	return render_template('branch_manage_staffs.html',data=data)

@branch.route('/branch_manage_deliveryboy',methods=['get','post'])
def branch_manage_deliveryboy():
	data={}
	bid=session['bid']
	bname=session['bname']
	data['bname']=bname
	data['bid']=bid
	q="select * from branches"
	data['branch']=select(q)
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		ph=request.form['phone']
		email=request.form['email']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s'"%(uname)
		res=select(q)
		if res:
			flash('THIS USER NAME AND PASSWORD ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('branch.branch_manage_deliveryboy'))
		else:
			q="insert into login values('%s','%s','dboy')"%(uname,password)
			lid=insert(q)			
			q="insert into deliveryboys values(NULL,'%s','%s','%s','%s','%s','%s')"%(uname,fname,lname,bid,ph,email)
			insert(q)
			return redirect(url_for('branch.branch_manage_deliveryboy'))
	q="select * from deliveryboys inner join login using(username) where branch_id='%s' order by first_name"%(bid)
	res=select(q)
	if res:
		data['deliveryboys']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='resigned':
		q="update login set user_type='resigned' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_manage_deliveryboy'))
	if action=='active':
		q="update login set user_type='dboy' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_manage_deliveryboy'))
	if action=='inactive':
		q="update login set user_type='inactive' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_manage_deliveryboy'))
	if action=='delete':
		q="delete from deliveryboys where boy_id='%s'"%(id)
		delete(q)
		return redirect(url_for('branch.branch_manage_deliveryboy'))
	if action=='update':
		q="select * from deliveryboys where boy_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		ph=request.form['phone']
		email=request.form['email']
		branch=request.form['branch']
		q="update deliveryboys set branch_id='%s',first_name='%s',last_name='%s',phone='%s',email='%s' where boy_id='%s'"%(branch,fname,lname,ph,email,id)
		update(q)
		if int(branch)!=int(bid):
			flash(fname+" transfer updated")
		else:
			flash("UPDATED SUCCESFULLY")
		return redirect(url_for('branch.branch_manage_deliveryboy'))

	if 'find' in request.form:
		search=request.form['search']+'%'
		q="select * from deliveryboys inner join login using(username) where first_name like '%s' and branch_id='%s' order by first_name"%(bid,search)
		res=select(q)
		if res:
			data['deliveryboys']=res
			print(res)
		else:
			flash("NO RESULTS FOUND")
			return redirect(url_for('branch.branch_manage_staffs'))
	return render_template('branch_manage_deliveryboy.html',data=data)


@branch.route('branch_reg_cus',methods=['get','post'])
def branch_reg_cus():
	data={}
	q="select * from customers order by first_name "
	res=select(q)
	data['customers']=res
	return render_template('branch_reg_cus.html',data=data)

@branch.route('/branch_view_bookings',methods=['get','post'])
def branch_view_bookings():
	data={}
	bid=session['bid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select * from bookings inner join customers using(customer_id) where from_branch='%s' or to_branch='%s'"%(bid,bid)
	session['mains']=q
	res=select(q)
	data['booking']=res
	q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and (booking_status !='Pending' AND booking_status!='Cancelled') "%(bid,bid)
	print(q)

	res=select(q)
	data['total']=res[0]['sum']
	session['sum']=data['total']
	print(res)
	if 'submit' in request.form:
		ty=request.form['type']
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		if ty=='all':
			if from_date:
				q="select * from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and( booking_date between '%s' and '%s')"%(bid,bid,from_date,to_date)
				print(q)
				session['mains']=q
				res=select(q)
				data['booking']=res
				print(res)
				q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and ( booking_date between '%s' and '%s') and (booking_status !='Pending') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(bid,bid,from_date,to_date)
				res=select(q)
				data['total']=res[0]['sum']
				session['sum']=data['total']
				print(data['total'])
			else:
				q="select * from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s')"%(bid,bid)
				print(q)
				res=select(q)
				data['booking']=res
				session['mains']=q
				print(res)
				q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and  (booking_status !='Pending') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(bid,bid)
				res=select(q)
				data['total']=res[0]['sum']
				session['sum']=data['total']
				print(data['total'])
		else:
			if from_date:
				q="select * from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and( booking_date between '%s' and '%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(bid,bid,from_date,to_date)
				print(q)
				res=select(q)
				data['booking']=res
				session['mains']=q
				print(res)
				q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and ( booking_date between '%s' and '%s') and (booking_status !='Pending') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(bid,bid,from_date,to_date)
				res=select(q)
				data['total']=res[0]['sum']
				session['sum']=data['total']
				print(data['total'])
			else:
				q="select * from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(bid,bid)
				print(q)
				res=select(q)
				data['booking']=res
				print(res)
				q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (from_branch='%s' or to_branch='%s') and  (booking_status !='Pending') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(bid,bid)
				res=select(q)
				data['total']=res[0]['sum']
				session['sum']=data['total']
				print(data['total'])

	# print(res)
	# cid=session['cid']
	# q="select * from packages where pack_id='%s'"%(pid)
	# res=select(q)
	# data['price']=res
	# print(res)
	# if 'submit' in request.form:
	# 	kg=request.form['kg']
	# 	l=request.form['len']
	# 	width=request.form['width']
	# 	floc=request.form['floc']
	# 	tloc=request.form['tloc']
	# 	brid=request.form['bid']
	# 	q="select * from bookings"
	# 	res=select(q)
	# 	if res:
	# 		s="B__"
	# 		prebid=res[0]['booking_id'].split("__")
	# 		print(prebid)
	# 		bid=int(prebid[1])+1
	# 		bid="B__"+str(bid)
	# 		print(bid)
	# 	else:
	# 		bid="B__1"
	# 	q="insert into bookings values('%s','%s',NOW(),'%s','%s','%s','%s','%s','%s','Pending','Pending','Pending')"%(bid,cid,brid,kg,l,width,floc,tloc)
	# 	print(q)
	# 	lid=insert(q)
	# 	flash("booked sucessfully")
	# 	return redirect(url_for('branch.branch_view_bookings',id=pid))

	return render_template('branch_view_bookings.html',data=data)


@branch.route('/branch_dboyrqt',methods=['get','post'])
def branch_dboyrqt():
	data={}
	bid=session['bid']
	data['bid']=bid
	username=session['username']
	q="select * from resign_request inner join deliveryboys using(username) inner join login using(username) where branch_id='%s'"%(bid)
	res=select(q)
	print(q)
	data['request']=res

	if 'action1' in request.args:
		action1=request.args['action1']
		print(action1)
		id=request.args['id']
		
	else:
		action1=None
	if action1=='accept':
		q="update login set user_type='resigned' where username='%s'"%(id)
		update(q)
		q="update resign_request set status='accepted' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_dboyrqt'))
	if action1=='decline':

		q="update resign_request set status='declined' where username='%s'"%(id)
		print(q)
		update(q)
		return redirect(url_for('branch.branch_dboyrqt'))

	
	
	return render_template('branch_dboyrqt.html',data=data)



@branch.route('/branch_staffrqt',methods=['get','post'])
def branch_staffrqt():
	data={}
	bid=session['bid']
	data['bid']=bid
	username=session['username']
	q="select * from resign_request inner join staffs using(username) inner join login using(username) where branch='%s'"%(bid)
	res=select(q)
	print(q)
	data['request']=res

	if 'action1' in request.args:
		action1=request.args['action1']
		print(action1)
		id=request.args['id']
		
	else:
		action1=None
	if action1=='accept':
		q="update login set user_type='resigned' where username='%s'"%(id)
		update(q)
		q="update resign_request set status='accepted' where username='%s'"%(id)
		update(q)
		return redirect(url_for('branch.branch_staffrqt'))
	if action1=='decline':

		q="update resign_request set status='declined' where username='%s'"%(id)
		print(q)
		update(q)
		return redirect(url_for('branch.branch_staffrqt'))
	return render_template('branch_staffrqt.html',data=data)



@branch.route('/branch_print',methods=['get','post'])
def branch_print():
	data={}

	q="select * from branches"
	res=select(q)
	data['branch']=res
	res=select(session['mains'])
	data['booking']=res
	data['total']=session['sum']
	
	return render_template('branch_print.html',data=data)