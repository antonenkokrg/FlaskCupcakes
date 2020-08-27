"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, flash, request, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

def serialize_cupcake(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route("/")
def root():

    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(ck) for ck in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<cupcake_id>")
def cupcake_info(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=serialize_cupcake(cupcake))

@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size,rating=rating,image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=serialized), 201 )


@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def edit_cupcake(cupcake_id):
    # cupcake = Cupcake.query.get_or_404(cupcake_id)

    # cupcake.flavor = request.json.get('flavor',cupcake.flavor)
    # cupcake.size = request.json.get("size",cupcake.size)
    # cupcake.rating = request.json.get("rating",cupcake.rating)
    # cupcake.image = request.json.get("image",cupcake.image)
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data.get('flavor',cupcake.flavor)
    cupcake.rating = data.get('rating',cupcake.rating)
    cupcake.size = data.get('size',cupcake.size)
    cupcake.image = data.get('image',cupcake.image)
    db.session.commit()

    return jsonify(cupcake=serialize_cupcake(cupcake))

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")