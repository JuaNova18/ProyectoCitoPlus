from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

#start app
app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

#Credential to access
users = {
  "admin": "12345"
}

#Verification password method
@auth.verify_password
def verify_password(username, password):
  if username in users and users[username] == password:
    return username
  
#create database model for users
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), nullable=False)
  phone = db.Column(db.String(10), nullable=False)
  rol = db.Column(db.String(50), nullable=False)

  def serialize(self):
    return {
      'id':self.id,
      'name':self.name,
      'email':self.email,
      'phone':self.phone,
      'rol':self.rol
    }
#creating automaticly database tables
with app.app_context():
  db.create_all()
#create routes
@app.route('/users', methods = ['GET'])
@auth.login_required
def get_users():
  users = User.query.all()
  return jsonify({'users': [user.serialize() for user in users]})

@app.route('/users', methods = ['POST'])
@auth.login_required
def create_users():
  data = request.get_json()
  user = User(name = data['name'],
                    email = data['email'],
                    phone = data['phone'],
                    rol = data['rol'])
  db.session.add(user)
  db.session.commit()
  return jsonify({'message':'Se creó un usuario', 'user': user.serialize()}), 201

#obtain only one item
@app.route('/users/<int:id>', methods = ['GET'])
@auth.login_required
def get_contact(id):
  user = User.query.get(id)
  if not user:
    return jsonify({'message':'Contacto no encontrado'}), 404
  return jsonify(user.serialize())
#update data with id
@app.route('/users/<int:id>', methods = ['PUT', 'PATCH'])
@auth.login_required
def update_contact(id):
  user = User.query.get_or_404(id)
  #obtain data from json request
  data = request.get_json()
  #update data
  if 'name' in data:
    user.name = data['name']
  if 'email' in data:
    user.email = data['email']
  if 'phone' in data:
    user.phone = data['phone']
  if 'rol' in data:
    user.rol = data['rol']
  #save data on database
  db.session.commit()
  #return a message with object json changes
  return jsonify({'message':'Usuario actualizado con éxito', 'user':user.serialize()}), 201
#delete data
@app.route('/users/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_user(id):
  user = User.query.get(id)
  if not user:
    return jsonify({'message':'Usuario no encontrado'}), 404
  #delete data
  db.session.delete(user  )
  db.session.commit()
  return jsonify({'message':'Usuario eliminado con éxito'})
#create database model for visitors
class Visitor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), nullable=False)
  number_id = db.Column(db.String(50), nullable=False)
  registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def serialize(self):
    return {
      'id':self.id,
      'name':self.name,
      'number_id':self.number_id,
      'registration_date':self.registration_date,
    }
#it's create automaticly the database tables
with app.app_context():
  db.create_all()
#creating routes
@app.route('/visitors', methods = ['GET'])
@auth.login_required
def get_visitors():
  visitors = Visitor.query.all()
  return jsonify({'visitors': [visitor.serialize() for visitor in visitors]})

@app.route('/visitors', methods = ['POST'])
@auth.login_required
def create_visitor():
  data = request.get_json()
  visitor = Visitor(name = data['name'],
                    email = data['email'],
                    number_id = data['number_id'])
  db.session.add(visitor)
  db.session.commit()
  return jsonify({'message':'Se creó un visitante', 'visitante': visitor.serialize()}), 201

#obtain only one element
@app.route('/visitors/<int:id>', methods = ['GET'])
@auth.login_required
def get_visitor(id):
  visitor = Visitor.query.get(id)
  if not visitor:
    return jsonify({'message':'Visitante no encontrado'}), 404
  return jsonify(visitor.serialize())
#update data with id
@app.route('/visitors/<int:id>', methods = ['PUT', 'PATCH'])
@auth.login_required
def update_visitor(id):
  visitor = Visitor.query.get_or_404(id)
  #recive data from json request
  data = request.get_json()
  #changing data
  if 'name' in data:
    visitor.name = data['name']
  if 'email' in data:
    visitor.email = data['email']
  if 'number_id' in data:
    visitor.number_id = data['number_id']
  #save data on the database
  db.session.commit()
  #return a message about json object 
  return jsonify({'message':'Visitante actualizado con éxito', 'visitante':visitor.serialize()}), 201
#delete data
@app.route('/visitors/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_visitor(id):
  visitor = Visitor.query.get(id)
  if not visitor:
    return jsonify({'message':'Visitante no encontrado'}), 404
  #delete data
  db.session.delete(visitor  )
  db.session.commit()
  return jsonify({'message':'Visitante eliminado con éxito'})