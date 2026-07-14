"""CarVerse — Flask application entry point."""
from flask import Flask, render_template
from sqlalchemy import text
from config import Config
from models import db, Car, EngineType, EngineVariant
from api import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()
        _migrate_old_engines()

    @app.route("/")
    def index():
        featured = Car.query.order_by(Car.horsepower.desc()).limit(6).all()
        latest = Car.query.order_by(Car.created_at.desc()).limit(4).all()
        categories = [
            "Legendary", "Production", "Concept", "Hypercar", "Supercar",
            "Sports", "Electric", "Luxury", "Common", "Classic", "Racing",
        ]
        return render_template("index.html", featured=featured,
                               latest=latest, categories=categories)

    @app.route("/car/<int:car_id>")
    def car_page(car_id):
        return render_template("car_details.html",
                               car=Car.query.get_or_404(car_id))

    @app.route("/edit/<int:car_id>")
    def edit_page(car_id):
        return render_template("edit.html", car=Car.query.get_or_404(car_id))

    @app.route("/category/<name>")
    def category_page(name):
        cars = Car.query.filter(Car.category == name).all()
        return render_template("category.html", name=name, cars=cars)

    @app.route("/admin")
    def admin_page():
        return render_template("admin.html")

    @app.route("/api/stats")
    def api_stats():
        return {
            "cars": Car.query.count(),
            "brands": db.session.query(Car.brand).distinct().count(),
            "engines": EngineVariant.query.count(),
            "categories": db.session.query(Car.category).distinct().count(),
        }

    return app


def _migrate_old_engines():
    """Migrates the old flat engines table into EngineType and EngineVariant tables."""
    if EngineType.query.count() > 0:
        return
    if "engines" not in db.inspect(db.engine).get_table_names():
        return
    rows = db.session.execute(text("SELECT * FROM engines")).mappings().all()
    for row in rows:
        layout = (row.get("layout") or "Other").strip() or "Other"
        etype = EngineType.query.filter_by(name=layout).first()
        if not etype:
            etype = EngineType(name=layout)
            db.session.add(etype)
            db.session.flush()
        db.session.add(EngineVariant(
            engine_type_id=etype.id,
            name=row.get("name") or layout,
            power_hp=row.get("power_hp") or 0,
            torque_nm=row.get("torque_nm") or 0,
            weight_kg=row.get("weight_kg") or 0,
            image_url=row.get("image_url") or "",
        ))
    db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)