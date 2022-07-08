from flask import *
from database import *
import uuid
admin=Blueprint('admin',__name__)
 

@admin.route('/adminhome',methods=['get','post'])
def adminhome():
	return render_template('adminhome.html')



@admin.route('/admin_manage_branches',methods=['get','post'])
def admin_manage_branches():
	data={}
	if 'submit' in request.form:
		bname=request.form['bname']
		lat=request.form['lat']
		lon=request.form['lon']
		ph=request.form['phone']
		email=request.form['email']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s'"%(uname)
		res=select(q)
		
		if res:
			flash('THIS USER NAME ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('admin.admin_manage_branches'))
		else:
			q="select * from branches where phone='%s' or email='%s'"%(ph,email)
			res1=select(q)

			q="select * from deliveryboys where phone='%s' or email='%s'"%(ph,email)
			res2=select(q)
			q="select * from staffs where phone='%s' or email='%s'"%(ph,email)
			res3=select(q)
			if res1 or res2 or res3:
				flash("ALREADY YOU HAVE AN ACCOUNT")
				return redirect(url_for('admin.admin_manage_branches'))
			else:
				q="insert into login values('%s','%s','branch')"%(uname,password)
				lid=insert(q)
				
				q="insert into branches values(NULL,'%s','%s','%s','%s','%s','%s')"%(uname,bname,lat,lon,ph,email,)
				insert(q)
				return redirect(url_for('admin.admin_manage_branches'))
	q="select * from branches inner join login using(username)"
	res=select(q)
	if res:
		data['branch']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
		print(action)
		print("%%%%%%%%%%%%%%%%")
	else:
		action=None
	if action=='delete':
		q="delete from branches where branch_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_branches'))
	if action=='update':
		q="select * from branches where branch_id='%s'"%(id)
		data['updater']=select(q)
	if action=='active':
		q="update login set user_type='branch' where username='%s'"%(id)
		# z1="select * from staffs inner join login using(username) where username='%s'"%(id)
		# z2="select * from deliveryboys inner join login using(username) where username='%s'"%(id)
		# res=select(z1)
		# if res:
		# 	sid=
		#     z1="update login set user_type='staff' where username='%s'"%(sid)
		update(q)
		return redirect(url_for('admin.admin_manage_branches'))
	if action=='inactive':
		q="update login set user_type='inactive' where username='%s'"%(id)
		update(q)
		q="select branch_id from branches where username='%s'"%(id)
		res=select(q)
		branch_id=res[0]['branch_id']
		q="(SELECT username FROM deliveryboys  WHERE branch_id='%s') UNION (SELECT username FROM staffs  WHERE branch='%s') "%(branch_id,branch_id)
		res=select(q)
		for row in res:
			username=row['username']
			q="update login set user_type='inactive' where username='%s'"%(username)
			update(q)
		return redirect(url_for('admin.admin_manage_branches'))
	if 'update' in request.form:
		bname=request.form['bname']
		lat=request.form['lat']
		lon=request.form['lon']
		ph=request.form['phone']
		email=request.form['email']
		q="update branches set branch_name='%s',latitude='%s',longitude='%s',phone='%s',email='%s' where branch_id='%s'"%(bname,lat,lon,ph,email,id)
		update(q)
		return redirect(url_for('admin.admin_manage_branches'))
	return render_template('admin_manage_branches.html',data=data)


@admin.route('/admin_view_branch',methods=['get','post'])
def admin_view_branch():
	data={}
	
	q="select * from branches inner join login using(username) where user_type='branch'"
	res=select(q)
	if res:
		data['branch']=res
		print(res)

	if 'submit' in request.form:
		search=request.form['search']+'%'
		q="select * from branches inner join login using(username) where user_type='branch' and branch_name like '%s'"%(search)
		res=select(q)
		if res:
			data['branch']=res
		else:
			flash("NO RESULTS FOUND")
			return redirect(url_for('admin.admin_view_branch'))

	return render_template('admin_view_branch.html',data=data)





@admin.route('/admindboy',methods=['get','post'])
def admindboy():
	data={}
	data['bname']=request.args['bname']
	id=request.args['id']
	q="select * from deliveryboys inner join login using(username) where branch_id='%s'  order by first_name"%(id)
	# q="select * from deliveryboys inner join login using(username) where branch_id='%s' and user_type='dboy' order by first_name"%(id)
	res=select(q)
	if res:
		data['deliveryboys']=res
		print(res)
	
	
	return render_template('admindboy.html',data=data)




@admin.route('/adminviewstaff',methods=['get','post'])
def adminviewstaff():
	data={}
	data['bname']=request.args['bname']
	id=request.args['id']
	
	q="select * from staffs inner join login using(username) where branch='%s' order by first_name"%(id)
	res=select(q)
	if res:
		data['staffs']=res
		print(res)
	
	return render_template('adminviewstaff.html',data=data)



@admin.route('/admin_manage_cargo_packages',methods=['get','post'])
def admin_manage_cargo_packages():
	data={}
	if 'submit' in request.form:
		packname=request.form['packname']
		maxkg=request.form['maxkg']
		maxh=request.form['maxh']
		maxw=request.form['maxw']
		maxkm=request.form['maxkm']
		maxp=request.form['maxp']
		
		q="insert into packages values(NULL,'%s','%s','%s','%s','%s','%s','active')"%(packname,maxkg,maxh,maxw,maxkm,maxp)
		insert(q)
		return redirect(url_for('admin.admin_manage_cargo_packages'))

	q="select * from packages"
	res=select(q)
	if res:
		data['price']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update packages set pstatus='active' where pack_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_cargo_packages'))
	if action=='inactive':
		q="update packages set pstatus='inactive' where pack_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_cargo_packages'))
	if action=='delete':
		q="delete from packages where pack_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_cargo_packages'))
	if action=='update':
		q="select * from packages where pack_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		packname=request.form['packname']
		maxkg=request.form['maxkg']
		maxh=request.form['maxh']
		maxw=request.form['maxw']
		maxkm=request.form['maxkm']
		maxp=request.form['maxp']
		q="update packages set packname='%s',maximum_weight='%s',maximum_height='%s',maximum_width='%s',maximum_distance='%s',minimum_price='%s' where pack_id='%s'"%(packname,maxkg,maxh,maxw,maxkm,maxp,id)
		update(q)
		return redirect(url_for('admin.admin_manage_cargo_packages'))
	return render_template('admin_manage_cargo_packages.html',data=data)


@admin.route('/admin_view_feedback',methods=['get','post'])
def admin_view_feedback():
	data={}
	q="SELECT * FROM feedback INNER JOIN branches using(branch_id) inner join customers using(customer_id)"
	res=select(q)
	data['feedbacks']=res
	print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
		if action=="update":
			q="select * from feedback inner join customers using(customer_id) where feedback_id='%s' "%(id)
			res=select(q)
			data['updater']=res
	if 'update' in request.form:
		reply=request.form['reply']
		q="update feedback set reply='%s' where feedback_id='%s'"%(reply,id)
		update(q)
		return redirect(url_for('admin.admin_view_feedback'))
	return render_template('admin_view_feedback.html',data=data)


@admin.route('/admin_review_andrate',methods=['get','post'])
def admin_review_andrate():
	data={}
	q="select * from review_rating inner join branches using(branch_id) inner join customers using(customer_id)"
	res=select(q)
	print(res)
	data['rating']=res
	print(res)
	# q="select * from feedback inner join branches using(branch_id) where admin_id='%s'"%(cid)	
	# res=select(q)
	# data['fb']=res
	# print(res)
	return render_template('admin_review_andrate.html',data=data)

@admin.route('/admin_view_booking',methods=['get','post'])
def admin_view_booking():
	data={}
	session['branch_id']=0
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select * from bookings inner join customers using(customer_id)"
	session['mains']=q
	res=select(q)
	data['booking']=res
	q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where  (booking_status !='Pending' AND booking_status!='Cancelled') "
	res=select(q)
	data['total']=res[0]['sum']
	session['sum']=data['total']
	print(res)
	if 'submit' in request.form:
		ty=request.form['type']
		branch=request.form['branch']
		tbranch=request.form['tbranch']
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		print("7777777777777777")
		print(from_date)
		

		
		
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		if ty=='all':
			if from_date:		
				if branch =='no':
					print("^^^^^^^^^^^^^^^^")

					q="select * from bookings inner join customers using(customer_id) where( booking_date between '%s' and '%s')"%(from_date,to_date)
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res
					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where ( booking_date between '%s' and '%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(from_date,to_date)
					res=select(q)
					data['total']=res[0]['sum']
					session['sum']=data['total']
					print(data['total'])
				else:
					q="select * from bookings inner join customers using(customer_id) where( booking_date between '%s' and '%s') and (from_branch='%s' and to_branch='%s')"%(from_date,to_date,branch,tbranch)
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res
					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where ( booking_date between '%s' and '%s') and (booking_status !='Pending' AND booking_status!='Cancelled') and (from_branch='%s' and to_branch='%s')"%(from_date,to_date,branch,tbranch)
					res=select(q)
					data['total']=res[0]['sum']
					print(data['total'])
					session['sum']=data['total']
					data['bran_id']=branch
					session['branch_id']=branch
			else:
				if branch =='no':
					print("^^^^^^^^^^^^^^^^")

					q="select * from bookings inner join customers using(customer_id) "
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res

					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (booking_status !='Pending' AND booking_status!='Cancelled')"
					res=select(q)
					data['total']=res[0]['sum']
					session['sum']=data['total']
					print(data['total'])
				else:
					q="select * from bookings inner join customers using(customer_id) where (from_branch='%s' and to_branch='%s')"%(branch,tbranch)
					print(q)
					res=select(q)
					data['booking']=res
					session['mains']=q

					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (booking_status !='Pending' AND booking_status!='Cancelled') and (from_branch='%s' and to_branch='%s')"%(branch,tbranch)
					res=select(q)
					data['total']=res[0]['sum']
					print(data['total'])
					session['sum']=data['total']
					data['bran_id']=branch
					session['branch_id']=branch
				

		else:
			if from_date:		
				if branch =='no':
					print("^^^^^^^^^^^^^^^^")

					q="select * from bookings inner join customers using(customer_id) where( booking_date between '%s' and '%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(from_date,to_date)
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res
					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where ( booking_date between '%s' and '%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(from_date,to_date)
					res=select(q)
					data['total']=res[0]['sum']
					session['sum']=data['total']
					print(data['total'])
				else:
					q="select * from bookings inner join customers using(customer_id) where( booking_date between '%s' and '%s') and (from_branch='%s' and to_branch='%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(from_date,to_date,branch,tbranch)
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res
					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where ( booking_date between '%s' and '%s') and (booking_status !='Pending' AND booking_status!='Cancelled') and (from_branch='%s' and to_branch='%s')"%(from_date,to_date,branch,tbranch)
					res=select(q)
					data['total']=res[0]['sum']
					print(data['total'])
					session['sum']=data['total']
					data['bran_id']=branch
					session['branch_id']=branch
			else:
				if branch =='no':
					print("^^^^^^^^^^^^^^^^")

					q="select * from bookings inner join customers using(customer_id) where (booking_status !='Pending' AND booking_status!='Cancelled')"
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res
					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (booking_status !='Pending' AND booking_status!='Cancelled')"
					res=select(q)
					data['total']=res[0]['sum']
					session['sum']=data['total']
					print(data['total'])
				else:
					q="select * from bookings inner join customers using(customer_id) where (from_branch='%s' and to_branch='%s') and (booking_status !='Pending' AND booking_status!='Cancelled')"%(branch,tbranch)
					print(q)
					session['mains']=q
					res=select(q)
					data['booking']=res
					print(res)
					q="select *,sum(amount) as sum from bookings inner join customers using(customer_id) where (booking_status !='Pending' AND booking_status!='Cancelled') and (from_branch='%s' and to_branch='%s')"%(branch,tbranch)
					res=select(q)
					data['total']=res[0]['sum']
					session['sum']=data['total']
					print(data['total'])
					data['bran_id']=branch
					session['branch_id']=branch
				



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

	return render_template('admin_view_booking.html',data=data)

@admin.route('/admin_print',methods=['get','post'])
def admin_print():
	data={}

	branch=session['branch_id']
	print("&&&&&&&&&&&&&&&&&&&")
	print(branch)
	if int(branch)!=0:
		data['bran_id']=branch
	q="select * from branches"
	res=select(q)
	data['branch']=res
	res=select(session['mains'])
	data['booking']=res
	data['total']=session['sum']
	
	return render_template('admin_print.html',data=data)




@admin.route('admin_view_cus',methods=['get','post'])
def admin_view_cus():
	data={}
	q="select * from customers inner join login using(username) order by first_name "
	res=select(q)
	data['customers']=res

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
		print(action)
		print("%%%%%%%%%%%%%%%%")
	else:
		action=None

	
	if action=='active':
		q="update login set user_type='customer' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_view_cus'))
	if action=='inactive':
		q="update login set user_type='inactive' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_view_cus'))

	# if 'action1' in request.args:
	# 	action1=request.args['action1']
	# 	#id=request.args['id']
	# 	print(action1)
	# 	print("%%%%%%%%%%%%%%%%")
	# else:
	# 	action1=None

	# if action1=='active' :
	# 	# q="select * from customers inner join login using(username) order by first_name "
	# 	q="select * from login where user_type='customer'"
	# 	select(q)
	# 	data['customers']=res
	# 	return redirect(url_for('admin.admin_view_cusa'))
	# if action1=='inactive':
	# 	q="select * from customers inner join login using(username) order by first_name where login.user_type='inactive' "
	# 	update(q)
	# 	data['customers']=res
	# 	return redirect(url_for('admin.admin_view_cusb'))
	return render_template('admin_view_cus.html',data=data)

# @admin.route('admin_view_cusa',methods=['get','post'])
# def admin_view_cusa():
# 	data={}
# 	q="select * from login where user_type='customer'"
# 	# res1=select(qq)
# 	# usr=res1
# 	# q="select * from customers inner join login using(username) order by first_name "
# 	res=select(q)
# 	data['customers']=res

# 	if 'action' in request.args:
# 		action=request.args['action']
# 		id=request.args['id']
# 		print(action)
# 		print("%%%%%%%%%%%%%%%%")
# 	else:
# 		action=None

# 	if action=='active':
# 		q="update login set user_type='customer' where username='%s'"%(id)
# 		update(q)
# 		return redirect(url_for('admin.admin_view_cusa'))
# 	if action=='inactive':
# 		q="update login set user_type='inactive' where username='%s'"%(id)
# 		update(q)
# 		return redirect(url_for('admin.admin_view_cusa'))
# 	return render_template('admin_view_cusa.html',data=data)

# @admin.route('admin_view_cusb',methods=['get','post'])
# def admin_view_cusb():
# 	data={}
# 	q="select * from login where user_type='customer'"
# 	# res1=select(qq)
# 	# usr=res1
# 	# q="select * from customers inner join login using(username) order by first_name "
# 	res=select(q)
# 	data['customers']=res

# 	if 'action' in request.args:
# 		action=request.args['action']
# 		id=request.args['id']
# 		print(action)
# 		print("%%%%%%%%%%%%%%%%")
# 	else:
# 		action=None

# 	if action=='active':
# 		q="update login set user_type='customer' where username='%s'"%(id)
# 		update(q)
# 		return redirect(url_for('admin.admin_view_cusb'))
# 	if action=='inactive':
# 		q="update login set user_type='inactive' where username='%s'"%(id)
# 		update(q)
# 		return redirect(url_for('admin.admin_view_cusb'))
# 	return render_template('admin_view_cusb.html',data=data)





# @admin.route('/admin_manage_landscape',methods=['get','post'])
# def admin_manage_landscape():
# 	data={}
# 	if 'submit' in request.form:
# 		lname=request.form['lname']
# 		q="select * from landscape where landscape='%s'"%(lname)
# 		res=select(q)
# 		if res:
# 			flash("THIS TYPE LANDSCAPE PLAN IS ALREADY ADDED")
# 		else:
# 			q="insert into landscape values(NULL,'%s')"%(lname)
# 			insert(q)
# 	q="select * from landscape"
# 	res=select(q)
# 	if res:
# 		data['landscape']=res
# 		print(res)
# 	if 'action' in request.args:
# 		action=request.args['action']
# 		id=request.args['id']
# 	else:
# 		action=None
# 	if action=='delete':
# 		q="delete from landscape where landscape_id='%s'"%(id)
# 		delete(q)
# 		return redirect(url_for('admin.admin_manage_landscape'))
# 	if action=='update':
# 		q="select * from landscape where landscape_id='%s'"%(id)
# 		data['updater']=select(q)
# 	if 'update' in request.form:
# 		uplname=request.form['uplname']
# 		q="update landscape set landscape='%s' where landscape_id='%s'"%(uplname,id)
# 		update(q)
# 		return redirect(url_for('admin.admin_manage_landscape'))
# 	return render_template('admin_manage_landscape.html',data=data)



# @admin.route('/admin_manage_district',methods=['get','post'])
# def admin_manage_district():
# 	data={}
# 	if 'submit' in request.form:
# 		name=request.form['name']
# 		q="select * from district where district='%s'"%(name)
# 		res=select(q)
# 		if res:
# 			flash("THIS DISTRICT PLAN IS ALREADY ADDED")
# 		else:
# 			q="insert into district values(NULL,'%s')"%(name)
# 			insert(q)
# 	q="select * from district"
# 	res=select(q)
# 	if res:
# 		data['district']=res
# 		print(res)
	
# 	return render_template('admin_manage_district.html',data=data)


# @admin.route('/admin_manage_places',methods=['get','post'])
# def admin_manage_places():
# 	data={}
# 	q="select * from landscape "
# 	data['landscape']=select(q)
# 	did=request.args['did']
# 	q="select * from type"
# 	data['type']=select(q)
# 	print(did)
# 	data['did']=did
# 	name=request.args['name']
# 	print(name)
# 	data['names']=name
# 	print(data["names"])
# 	if 'submit' in request.form:
# 		pname=request.form['name']
# 		des=request.form['des']
# 		lat=request.form['lat']
# 		lon=request.form['lon']
# 		typ=request.form['type']
# 		landscape=request.form['land']

# 		q="select * from place where placename='%s' and district_id='%s'"%(pname,did)
# 		res=select(q)
# 		if res:
# 			flash("THIS PLACE  IS ALREADY ADDED")
# 		else:
# 			q="insert into place values(NULL,'%s','%s','%s','%s','%s')"%(did,pname,des,lat,lon)
# 			res=insert(q)
# 			q="insert into placedetail values(NULL,'%s','%s','%s')"%(res,landscape,typ)
# 			print(q)
# 			print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
# 			insert(q)
			
# 			return redirect(url_for('admin.admin_manage_places',name=name,did=did))
# 	q="select * from place where district_id='%s'"%(did)
# 	res=select(q)
# 	if res:
# 		data['place']=res
# 		print(res)
# 	if 'action' in request.args:
# 		action=request.args['action']
# 		print(action)
# 		id=request.args['id']
# 	else:
# 		action=None
# 	if action=='delete':
# 		q="delete from place where place_id='%s'"%(id)
# 		delete(q)
# 		return redirect(url_for('admin.admin_manage_places',name=name,did=did))
# 	if action=='update':
# 		q="select * from place where place_id='%s'"%(id)
# 		data['updater']=select(q)
# 	if 'update' in request.form:
# 		upname=request.form['upname']
# 		q="update place set placename='%s' where place_id='%s'"%(upname,id)
# 		update(q)		
# 		return redirect(url_for('admin.admin_manage_places',name=name,did=did))
# 	if action=='images':
# 		print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
# 		q="select * from placeimage where place_id='%s'"%(id)
# 		res=select(q)
# 		print(res)
# 		li=[]
# 		for row in res:
# 			if row['filepath'].split(".")[-1]=='jpg':
# 				li=li+[row]
# 				print("************")
# 				print(li)
# 				data['images']=li

# 		data['img']="image"

# 	if action=='videos':
# 		print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
# 		q="select * from placeimage where place_id='%s'"%(id)
# 		res=select(q)
# 		print(res)
# 		li=[]
# 		for row in res:
# 			if row['filepath'].split(".")[-1]=='mp4':
# 				li=li+[row]
# 				print("************")
# 				print(li)
# 				data['video']=li

# 		data['vid']="video"

# 	if 'imgsubmit' in request.form:
# 		f=request.files['file']
# 		path='static/'+str(uuid.uuid4())+f.filename
# 		f.save(path)
# 		print("#####################################")
# 		print(f.filename)
# 		if f.filename.split(".")[-1]=='jpg':

# 			q="insert into placeimage values(NULL,'%s','%s')"%(id,path)
# 			insert(q)
# 			flash("image added sucessfully")
# 		else:
# 			flash("please choose jpg format file")
# 		return redirect(url_for('admin.admin_manage_places',name=name,did=did))


# 	if 'vidsubmit' in request.form:
# 		f=request.files['file']
# 		path='static/'+str(uuid.uuid4())+f.filename
# 		f.save(path)
# 		if f.filename.split(".")[-1]=="mp4":

# 			q="insert into placeimage values(NULL,'%s','%s')"%(id,path)
# 			insert(q)
# 			flash("video added sucessfully")
# 		else:
# 			flash("please choose mp4 file")
# 		return redirect(url_for('admin.admin_manage_places',name=name,did=did))

# 	return render_template('admin_manage_places.html',data=data,name=name,did=did)


# @admin.route('/admin_view_complaints',methods=['get','post'])
# def admin_view_complaints():
# 	data={}
# 	q="SELECT * FROM user INNER JOIN complaint USING(user_id)"
# 	res=select(q)
# 	data['complaints']=res
# 	if 'action' in request.args:
# 		action=request.args['action']
# 		id=request.args['id']
# 		if action=="update":
# 			q="select * from complaint inner join user using(user_id) where complaint_id='%s' "%(id)
# 			res=select(q)
# 			data['updater']=res
# 	if 'update' in request.form:
# 		reply=request.form['reply']
# 		q="update complaint set reply='%s' where complaint_id='%s'"%(reply,id)
# 		update(q)
# 		return redirect(url_for('admin.admin_view_complaints'))
# 	return render_template('admin_view_complaints.html',data=data)


# @admin.route('admin_viewbooks',methods=['get','post'])
# def admin_viewbooks():
# 	data={}
# 	q="select * from items inner join students using(student_id)"
# 	res=select(q)
# 	data['items']=res
# 	return render_template('admin_viewbooks.html',data=data)

# @admin.route('admin_viewexchangehistory',methods=['get','post'])
# def admin_viewexchangehistory():
# 	data={}
# 	q="SELECT * FROM `exchanges` INNER JOIN items USING (`item_id`) INNER JOIN `students` ON (students.`student_id`=`items`.`student_id`)"
# 	data['exchange']=select(q)
# 	return render_template('admin_viewexchangehistory.html',data=data)


# @admin.route('admin_viewpurchase',methods=['get','post'])
# def admin_viewpurchase():
# 	data={}
# 	q="SELECT * FROM purchase INNER JOIN items ON(purchase.`item_id`=`items`.`item_id`) INNER JOIN `students` ON `items`.`student_id`=`students`.`student_id` order by(items.item)"
# 	res=select(q)
# 	data['purchase']=res
# 	return render_template('admin_viewpurchase.html',data=data)