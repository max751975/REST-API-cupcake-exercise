from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()

connect_db(app)
db.create_all()


@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def show_list():
    """"Returns JSON with all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    """Returns JSON for cupcake with specific id"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates new cupcake and returns JSON of that new cupcake"""
    new_flavor = request.json['flavor']
    new_size = request.json['size']
    new_rating = request.json['rating']
    new_image = request.json['image']
    new_cupcake = Cupcake(flavor=new_flavor, size=new_size, rating=new_rating, image=new_image or None)
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Updates cupcake with given id and returns JSON of updated cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def remove_cupcake(id):
    """Deletes cupcake and
        Returns JSON of: {message: "Deleted"}"""
    cupcake= Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
    