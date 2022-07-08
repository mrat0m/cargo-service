from flask import *
from database import *
import uuid
dboy=Blueprint('dboy',__name__)
 

@dboy.route('/dboyhome',methods=['get','post'])
def dboyhome():
	dname=session['dname']
	did=session['did']
	print(dname)
	return render_template('dboyhome.html',dname=dname)


@dboy.route('/dboy_view_pickups',methods=['get','post'])
def dboy_view_pickups():
	data={}
	dname=session['dname']
	did=session['did']
	q="select * from bookings inner join customers using(customer_id) where from_branch in (select branch_id from deliveryboys where boy_id='%s') and booking_status in('Paid','pickedup')"%(did)
	res=select(q)
	print(q)
	# fb['']=res
	# b="selct branch_name from branches where branch_id='%s'"%(fb)
	data['works']=res
	print(res)
	
	if 'action' in request.args:
		id=request.args['id']
		action=request.args['action']
		if action=='pickedup':
			q="update bookings set booking_status='pickedup' where booking_id='%s'"%(id)
			update(q)
			flash("update as pickedup")
			return redirect(url_for('dboy.dboy_view_pickups'))
		if action=='arrived':
			q="update bookings set booking_status='arrived' where booking_id='%s'"%(id)
			update(q)
			flash("update as arrived")
			return redirect(url_for('dboy.dboy_view_pickups'))


	return render_template('dboy_view_pickups.html',data=data)


@dboy.route('/dboy_view_assigned_cargos',methods=['get','post'])
def dboy_view_assigned_cargos():
	data={}
	dname=session['dname']
	did=session['did']
	q="select * from bookings inner join customers using(customer_id) inner join packages using(pack_id) where boy_id='%s'"%(did)
	res=select(q)
	print(q)
	data['works']=res
	print(res)
	if 'action' in request.args:
		id=request.args['id']
		q="select * from cargo_status where booking_id='%s'"%(id)
		res=select(q)
		if res:
			data['status']=res
			data['id']=id
		else:
			data['status']='Pending'
			data['id']=id
		print(data['status'])
	if 'action2' in request.args:
		id=request.args['id']
		q="update bookings set booking_status='delivered' where booking_id='%s'"%(id)
		update(q)
		flash("update as delivered")
		return redirect(url_for('dboy.dboy_view_assigned_cargos'))

	if 'submit' in request.form:
		name=request.form['name']
		q="insert into cargo_status values(NULL,'%s','%s',NOW())"%(id,name)
		insert(q)
		flash("CARGO TRACKING STATUS UPDATED")
		return redirect(url_for('dboy.dboy_view_assigned_cargos'))


	return render_template('dboy_view_assigned_cargos.html',data=data)

@dboy.route('/dboy_send_resign',methods=['get','post'])
def dboy_send_resign():
	data={}
	username=session['username']
	q="select * from resign_request where username='%s'"%(username)
	res=select(q)
	data['request']=res
	if 'submit' in request.form:
		reason=request.form['reason']
		
		q="insert into resign_request values(NULL,'%s','%s','Pending',NOW())"%(username,reason)
		res=insert(q)
		return redirect(url_for('dboy.dboy_send_resign'))
	
	return render_template('deboy_send_resign.html',data=data)