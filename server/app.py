# server/app.py
from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, User, Recipe

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = "filesystem"

bcrypt = Bcrypt(app)
db.init_app(app)
migrate = Migrate(app, db)

# SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        new_user = User(
            username=data['username'],
            image_url=data.get('image_url'),
            bio=data.get('bio')
        )

        new_user.password_hash = data['password']

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return jsonify(
            id=new_user.id,
            username=new_user.username,
            image_url=new_user.image_url,
            bio=new_user.bio
        ), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 422

# CHECK_SESSION
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify(
            id=user.id,
            username=user.username,
            image_url=user.image_url,
            bio=user.bio
        ), 200
    return jsonify({"error": "Unauthorized"}), 401

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user:
        print(f"Attempting to authenticate user: {user.username} with password: {data.get('password')}")  # Debugging line
        if user.authenticate(data.get('password')):
            print(f"User {user.username} authenticated successfully.")  # Debugging line
            session['user_id'] = user.id
            return jsonify(
                id=user.id,
                username=user.username,
                image_url=user.image_url,
                bio=user.bio
            ), 200
    return jsonify({"error": "Invalid credentials"}), 401

# LOGOUT
@app.route('/logout', methods=['DELETE'])
def logout():
    if session.get('user_id'):
        session.pop('user_id')
        return "", 204
    return jsonify({"error": "Unauthorized"}), 401

# GET /recipes
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    user_id = session.get('user_id')
    print(f"User ID from session: {user_id}")  # Debugging line
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        return jsonify([{
            "title": r.title,
            "instructions": r.instructions,
            "minutes_to_complete": r.minutes_to_complete,
            "user": {
                "id": r.user.id,
                "username": r.user.username,
                "image_url": r.user.image_url,
                "bio": r.user.bio
            }
        } for r in recipes]), 200

    if request.method == 'POST':
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get('title'),
            instructions=data.get('instructions'),
            minutes_to_complete=data.get('minutes_to_complete'),
            user_id=user_id
        )
        db.session.add(new_recipe)
        try:
            db.session.commit()
        except Exception as e:
            return jsonify({"errors": [str(e)]}), 422
        return jsonify(
            title=new_recipe.title,
            instructions=new_recipe.instructions,
            minutes_to_complete=new_recipe.minutes_to_complete,
            user={
                "id": new_recipe.user.id,
                "username": new_recipe.user.username,
                "image_url": new_recipe.user.image_url,
                "bio": new_recipe.user.bio
            }
        ), 201


if __name__ == '__main__':
    app.run(debug=True)
