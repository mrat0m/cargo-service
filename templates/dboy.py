from flask import *
from database import *
import uuid
dboy=Blueprint('dboy',__name__)
 

@dboy.route('/dboyhome',methods=['get','post'])
def dboyhome():
	sname=session['sname']
	sid=session['sid']
	print(sname)

	return render_template('dboyhome.html',sname=sname)
