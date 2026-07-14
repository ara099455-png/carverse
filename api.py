"""CarVerse REST API blueprint — fits new models.py (weight/torque/top_speed)."""
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import or_
from models import db, Car, EngineType, EngineVariant, Material, Color, Build
from calculator import calculate

api = Blueprint("api", __name__, url_prefix="/api")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-Admin-Key", "")
        if key != current_app.config["ADMIN_KEY"]:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------- Search
@api.get("/search")
def search():
    q = request.args.get("q", "").strip()
    if len(q) < 1:
        return jsonify([])
    like = f"%{q}%"
    cars = Car.query.filter(or_(
        Car.brand.ilike(like),
        Car.model.ilike(like),
        Car.generation.ilike(like),
        Car.nickname.ilike(like),
        (Car.brand + " " + Car.model).ilike(like),
    )).limit(8).all()
    return jsonify([c.to_dict() for c in cars])


# ---------------------------------------------------------------- Cars
@api.get("/cars")
def list_cars():
    query = Car.query
    category = request.args.get("category")
    if category:
        query = query.filter(Car.category == category)
    if request.args.get("sort") == "latest":
        query = query.order_by(Car.created_at.desc())
    page = request.args.get("page", 1, type=int)
    per = min(request.args.get("per_page", 24, type=int), 100)
    pag = query.paginate(page=page, per_page=per, error_out=False)
    return jsonify({
        "cars": [c.to_dict() for c in pag.items],
        "total": pag.total, "pages": pag.pages, "page": page,
    })


@api.get("/cars/<int:car_id>")
def get_car(car_id):
    return jsonify(Car.query.get_or_404(car_id).to_dict(full=True))


@api.post("/cars")
@admin_required
def create_car():
    data = request.get_json(force=True)
    car = Car()
    for key, value in data.items():
        if hasattr(car, key) and key != "id":
            setattr(car, key, value)
    db.session.add(car)
    db.session.commit()
    return jsonify(car.to_dict(full=True)), 201


@api.put("/cars/<int:car_id>")
@admin_required
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    for key, value in request.get_json(force=True).items():
        if hasattr(car, key) and key != "id":
            setattr(car, key, value)
    db.session.commit()
    return jsonify(car.to_dict(full=True))


@api.delete("/cars/<int:car_id>")
@admin_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"deleted": car_id})


# ---------------------------------------------------------------- Engine Types & Variants
@api.get("/engine-types")
def list_engine_types():
    types = EngineType.query.order_by(EngineType.name).all()
    return jsonify([t.to_dict(with_variants=True) for t in types])


@api.post("/engine-types")
@admin_required
def create_engine_type():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Name required"}), 400
    existing = EngineType.query.filter_by(name=name).first()
    if existing:
        return jsonify(existing.to_dict(with_variants=True)), 200
    etype = EngineType(name=name, image_url=(data.get("image_url") or "").strip())
    db.session.add(etype)
    db.session.commit()
    return jsonify(etype.to_dict(with_variants=True)), 201


@api.delete("/engine-types/<int:type_id>")
@admin_required
def delete_engine_type(type_id):
    etype = EngineType.query.get_or_404(type_id)
    db.session.delete(etype)   # cascade deletes its variants too
    db.session.commit()
    return jsonify({"deleted": type_id})


@api.post("/engine-variants")
@admin_required
def create_engine_variant():
    data = request.get_json(force=True)
    if not data.get("engine_type_id"):
        return jsonify({"error": "engine_type_id required"}), 400
    variant = EngineVariant(**{k: v for k, v in data.items()
                               if hasattr(EngineVariant, k) and k != "id"})
    db.session.add(variant)
    db.session.commit()
    return jsonify(variant.to_dict()), 201


@api.delete("/engine-variants/<int:variant_id>")
@admin_required
def delete_engine_variant(variant_id):
    variant = EngineVariant.query.get_or_404(variant_id)
    db.session.delete(variant)
    db.session.commit()
    return jsonify({"deleted": variant_id})


# ---------------------------------------------------------------- Materials
@api.get("/materials")
def list_materials():
    return jsonify([x.to_dict() for x in Material.query.all()])


@api.post("/materials")
@admin_required
def create_material():
    data = request.get_json(force=True)
    item = Material(**{k: v for k, v in data.items()
                       if hasattr(Material, k) and k != "id"})
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@api.delete("/materials/<int:item_id>")
@admin_required
def delete_material(item_id):
    item = Material.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"deleted": item_id})


# ---------------------------------------------------------------- Colors
@api.get("/colors")
def list_colors():
    return jsonify([x.to_dict() for x in Color.query.all()])


@api.post("/colors")
@admin_required
def create_color():
    data = request.get_json(force=True)
    item = Color(**{k: v for k, v in data.items()
                    if hasattr(Color, k) and k != "id"})
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@api.delete("/colors/<int:item_id>")
@admin_required
def delete_color(item_id):
    item = Color.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"deleted": item_id})


# ---------------------------------------------------------------- Builds (save system)
@api.post("/builds")
def save_build():
    data = request.get_json(force=True)
    build = Build.query.filter_by(
        car_id=data["car_id"], client_key=data.get("client_key", "")).first()
    if not build:
        build = Build(car_id=data["car_id"],
                      client_key=data.get("client_key", ""))
        db.session.add(build)
    build.engine_id = data.get("engine_id")
    build.material_id = data.get("material_id")
    build.color_id = data.get("color_id")
    db.session.commit()
    return jsonify(build.to_dict())


@api.get("/builds/<int:car_id>")
def get_build(car_id):
    build = Build.query.filter_by(
        car_id=car_id, client_key=request.args.get("client_key", "")).first()
    return jsonify(build.to_dict() if build else {})


# ---------------------------------------------------------------- Calculator
@api.post("/calculate")
def calc():
    data = request.get_json(force=True)
    car = Car.query.get_or_404(data["car_id"])
    engine = EngineVariant.query.get(data["engine_id"]) if data.get("engine_id") else None
    material = Material.query.get(data["material_id"]) if data.get("material_id") else None
    return jsonify(calculate(car, engine, material))