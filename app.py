from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os 

app=Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "Database.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class food_details(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	packet_details = db.Column(db.String(500), nullable = False)
	weight = db.Column(db.Integer, nullable=False)
	time = db.Column(db.String(100), nullable=False)
	picked = db.Column(db.Boolean)
#change
db.create_all()

@app.route('/',methods=["POST","GET"])
@app.route('/index',methods=["POST","GET"])
def root():
	food = food_details.query.order_by(food_details.id).all()
	
	if request.form:
		form = request.form
		s = food_details(
			packet_details = form['packet_details'],
			 weight = form['weight'],
			  time = form['time'])
		db.session.add(s)
		db.session.commit()
		redirect ('/')

	return render_template('index.html',food=food)

@app.route('/task_delete/<id>')
def task_delete(id):
	food = food_details.query.filter_by(id=int(id)).first()
	db.session.delete(food)
	db.session.commit()
	redirect ('/')
	return render_template('index.html')

if __name__ == '__main__' :
	app.run(debug = True)