"""SQLAlchemy models for CarVerse (column names match car_details.html)."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)

    # Identity
    brand = db.Column(db.String(80), nullable=False, index=True)
    model = db.Column(db.String(120), nullable=False, index=True)
    generation = db.Column(db.String(80), default="", index=True)
    nickname = db.Column(db.String(120), default="", index=True)
    category = db.Column(db.String(40), default="Production", index=True)

    # Basic info
    production_years = db.Column(db.String(40), default="")
    status = db.Column(db.String(40), default="Production")
    country = db.Column(db.String(60), default="")
    manufacturer = db.Column(db.String(120), default="")

    # Performance
    horsepower = db.Column(db.Integer, default=0)
    torque = db.Column(db.Integer, default=0)
    top_speed = db.Column(db.Integer, default=0)
    accel_0_100 = db.Column(db.Float, default=0.0)
    quarter_mile = db.Column(db.Float, default=0.0)
    weight = db.Column(db.Integer, default=0)

    # Dimensions (mm)
    length = db.Column(db.Integer, default=0)
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    wheelbase = db.Column(db.Integer, default=0)

    # Engine
    engine_name = db.Column(db.String(120), default="")
    engine_code = db.Column(db.String(60), default="")
    engine_layout = db.Column(db.String(60), default="")
    displacement = db.Column(db.Float, default=0.0)
    cylinders = db.Column(db.Integer, default=0)
    aspiration = db.Column(db.String(60), default="")
    fuel_type = db.Column(db.String(40), default="Petrol")
    redline = db.Column(db.Integer, default=0)

    # Transmission
    transmission_type = db.Column(db.String(80), default="")
    gear_count = db.Column(db.Integer, default=0)
    drivetrain = db.Column(db.String(20), default="RWD")

    # Sales / market ("85500+" allowed)
    units_produced = db.Column(db.String(40), default="")
    units_sold = db.Column(db.String(40), default="")
    market_availability = db.Column(db.String(120), default="")
    msrp = db.Column(db.String(40), default="")
    launch_date = db.Column(db.String(40), default="")

    # Extra
    competitors = db.Column(db.Text, default="")
    awards = db.Column(db.Text, default="")
    historical_importance = db.Column(db.Text, default="")

    # Media
    image_url = db.Column(db.String(500), default="")
    gallery = db.Column(db.Text, default="")        # comma separated URLs
    video_url = db.Column(db.String(500), default="")

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def full_name(self):
        parts = [self.brand, self.model]
        if self.generation:
            parts.append(f"({self.generation})")
        return " ".join(parts)

    @property
    def power_to_weight(self):
        return round(self.horsepower / self.weight * 1000, 1) if self.weight else 0

    def to_dict(self, full=False):
        d = {
            "id": self.id, "brand": self.brand, "model": self.model,
            "generation": self.generation, "nickname": self.nickname,
            "category": self.category, "full_name": self.full_name,
            "image_url": self.image_url, "horsepower": self.horsepower,
            "top_speed": self.top_speed, "status": self.status,
        }
        if full:
            for c in self.__table__.columns:
                d[c.name] = getattr(self, c.name)
            d["power_to_weight"] = self.power_to_weight
            d["created_at"] = str(self.created_at) if self.created_at else ""
        return d


class EngineType(db.Model):
    """e.g. V8, Inline 6, W16 — sirf category, koi specs nahi."""
    __tablename__ = "engine_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    image_url = db.Column(db.String(500), default="")

    variants = db.relationship("EngineVariant", backref="engine_type",
                               lazy=True, cascade="all, delete-orphan")

    def to_dict(self, with_variants=False):
        d = {"id": self.id, "name": self.name, "image_url": self.image_url}
        if with_variants:
            d["variants"] = [v.to_dict() for v in self.variants]
        return d


class EngineVariant(db.Model):
    """e.g. '6.2L Turbocharged V8' — actual usable engine with specs."""
    __tablename__ = "engine_variants"
    id = db.Column(db.Integer, primary_key=True)
    engine_type_id = db.Column(db.Integer, db.ForeignKey("engine_types.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    power_hp = db.Column(db.Integer, default=0)
    torque_nm = db.Column(db.Integer, default=0)
    weight_kg = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), default="")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Material(db.Model):
    __tablename__ = "materials"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, default="")
    weight_factor = db.Column(db.Float, default=1.0)
    strength_factor = db.Column(db.Float, default=1.0)
    image_url = db.Column(db.String(500), default="")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Color(db.Model):
    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hex_code = db.Column(db.String(9), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Build(db.Model):
    __tablename__ = "builds"
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    engine_id = db.Column(db.Integer, db.ForeignKey("engine_variants.id"))
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"))
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"))
    client_key = db.Column(db.String(64), index=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}