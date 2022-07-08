from flask import *
from database import *
import uuid
staff=Blueprint('staff',__name__)
 

@staff.route('/staffhome',methods=['get','post'])
def staffhome():
	sname=session['sname']
	sid=session['sid']
	print(sname)

	return render_template('staffhome.html',sname=sname)

@staff.route('/staff_cargo_rqst',methods=['get','post'])
def staff_cargo_rqst():
	data={}
	sid=session['sid']
	q="select * from branches"
	res=select(q)
	data['branch']=res
	print(res)
	q="select branch from staffs where staff_id='%s'"%(sid)
	res=select(q)
	brid=res[0]['branch']
	data['branch_id']=brid
	
	q="select * from bookings inner join customers using(customer_id) inner join packages using(pack_id) where (from_branch='%s' or to_branch='%s') and (booking_status!='Cancelled') order by booking_id desc"%(brid,brid)
	res=select(q)
	data['booking']=res
	print(res)

	if 'action' in request.args:

		boid=request.args['id']
		q="select * from bookings inner join packages using(pack_id) where booking_id='%s'"%(boid)
		res=select(q)
		data['updater']=res
		print(res)
	if 'action2' in request.args:
		boid=request.args['id']
		q="select * from deliveryboys inner join login using(username) where branch_id='%s' and user_type='dboy'"%(brid)
		res=select(q)
		data['boy']=res
	if 'action3' in request.args:
		boid=request.args['id']
		q="update bookings set booking_status='dispatched' where booking_id='%s'"%(boid)
		update(q)
		return redirect(url_for('staff.staff_cargo_rqst'))
		
	if 'update' in request.form:
		kg=request.form['kg']
		l=request.form['h']
		w=request.form['w']
		amt=request.form['amt']
		q="update bookings set weight='%s',length='%s',width='%s',amount='%s' where booking_id='%s'"%(kg,l,w,amt,boid)
		print(q)
		lid=update(q) 
		flash("CONFIRMATION SUCESS")
		return redirect(url_for('staff.staff_cargo_rqst'))
	if 'submit' in request.form:
		dboy=request.form['dboy']
		q="update bookings set boy_id='%s',booking_status='Reached' where booking_id='%s' "%(dboy,boid)
		update(q)
		return redirect(url_for('staff.staff_cargo_rqst'))
	return render_template('staff_cargo_rqst.html',data=data)


@staff.route('/staff_send_resign',methods=['get','post'])
def staff_send_resign():
	data={}
	username=session['username']
	q="select * from resign_request where username='%s'"%(username)
	res=select(q)
	data['request']=res
	if 'submit' in request.form:
		reason=request.form['reason']
		
		q="insert into resign_request values(NULL,'%s','%s','Pending',NOW())"%(username,reason)
		res=insert(q)
		return redirect(url_for('staff.staff_send_resign'))
	
	return render_template('staff_send_resign.html',data=data)