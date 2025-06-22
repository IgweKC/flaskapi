# import lib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)

#name the database db which will be in the same path as your python file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# validate data
user_arg = reqparse.RequestParser()
user_arg.add_argument('name',type=str, required=True, help = "Name cannot be blank")
user_arg.add_argument('email',type=str, required=True, help = "Email cannot be blank")

# shape of the serialize data
userFields = {
    'id':fields.Integer,
    'name': fields.String,
    'email': fields.String
}

#Create a database shape
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True,nullable=False)
    email = db.Column(db.String(80), unique=True,nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email={self.email})"


class Users(Resource):

    # get serialized resource
    @marshal_with(userFields)
    def get(slef):
        users = UserModel.query.all()
        return users
    
    # post serialized resource
    @marshal_with(userFields)
    def post(self):
        args = user_arg.parse_args()
        user = UserModel(name = args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

        #process data

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message =f"user id {id} not found")
        return user
    

    @marshal_with(userFields)
    def patch(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message =f"user id {id} not found")
        args = user_arg.parse_args()
        user.name = args['name']
        user.email=args['email']
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message =f"user id {id} not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel().query.all()
        return users

api.add_resource(Users,'/api/users/')
api.add_resource(User,'/api/users/<int:id>')

# create where you will request data from
@app.route('/')
def home():
    return'<h1>Flask Rest API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
