"""Seed CarVerse. Run: python seed.py"""
from app import create_app
from models import db, Car, Engine, Material, Color

CARS = [
    dict(brand="Ferrari", model="LaFerrari", generation="F150", nickname="The Ferrari",
         category="Hypercar", production_years="2013–2016", status="Discontinued",
         country="Italy", manufacturer="Ferrari S.p.A.", horsepower=963, torque=900,
         top_speed=350, accel_0_100=2.6, quarter_mile=9.7, weight=1585,
         length=4702, width=1992, height=1116, wheelbase=2650,
         engine_name="F140 FE V12 Hybrid", engine_code="F140FE", engine_layout="V12 Hybrid",
         displacement=6.3, cylinders=12, aspiration="Naturally Aspirated",
         fuel_type="Petrol Hybrid", redline=9250, transmission_type="7-speed DCT",
         gear_count=7, drivetrain="RWD", units_produced="499", units_sold="499",
         market_availability="Global (sold out)", msrp="$1,420,000",
         launch_date="2013-03-05", competitors="McLaren P1, Porsche 918 Spyder",
         awards="Hypercar of the Decade",
         historical_importance="Ferrari's first hybrid hypercar — Holy Trinity era flagship.",
         image_url="https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=1200"),
    dict(brand="Bugatti", model="Chiron", generation="Sport", category="Hypercar",
         production_years="2016–2024", status="Discontinued", country="France",
         manufacturer="Bugatti Automobiles", horsepower=1500, torque=1600,
         top_speed=420, accel_0_100=2.4, quarter_mile=9.4, weight=1996,
         length=4544, width=2038, height=1212, wheelbase=2711,
         engine_name="8.0L Quad-Turbo W16", engine_code="W16", engine_layout="W16",
         displacement=8.0, cylinders=16, aspiration="Quad-Turbocharged",
         fuel_type="Petrol", redline=6700, transmission_type="7-speed DSG",
         gear_count=7, drivetrain="AWD", units_produced="500", units_sold="500",
         market_availability="Global (sold out)", msrp="$3,000,000",
         launch_date="2016-03-01", competitors="Koenigsegg Jesko, Pagani Huayra",
         awards="", historical_importance="Successor to the Veyron — a 1,500 hp statement.",
         image_url="https://images.unsplash.com/photo-1566473965997-3de9c817e938?w=1200"),
    dict(brand="BMW", model="M5", generation="F90", nickname="Business Rocket",
         category="Sports", production_years="2017–2024", status="Discontinued",
         country="Germany", manufacturer="BMW M GmbH", horsepower=600, torque=750,
         top_speed=305, accel_0_100=3.4, quarter_mile=11.1, weight=1855,
         length=4965, width=1903, height=1473, wheelbase=2982,
         engine_name="S63 4.4L Twin-Turbo V8", engine_code="S63B44T4", engine_layout="V8",
         displacement=4.4, cylinders=8, aspiration="Twin-Turbocharged",
         fuel_type="Petrol", redline=7200, transmission_type="8-speed Automatic",
         gear_count=8, drivetrain="AWD", units_produced="40000+", units_sold="40000+",
         market_availability="Global", msrp="$104,000", launch_date="2017-08-21",
         competitors="Mercedes-AMG E63 S, Audi RS7", awards="",
         historical_importance="First M5 with M xDrive AWD.",
         image_url="https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=1200"),
    dict(brand="Toyota", model="Supra", generation="A80", nickname="Mk4 Supra",
         category="Legendary", production_years="1993–2002", status="Discontinued",
         country="Japan", manufacturer="Toyota", horsepower=326, torque=440,
         top_speed=285, accel_0_100=4.6, quarter_mile=13.1, weight=1570,
         length=4514, width=1811, height=1275, wheelbase=2550,
         engine_name="2JZ-GTE Twin-Turbo I6", engine_code="2JZ-GTE",
         engine_layout="Inline 6", displacement=3.0, cylinders=6,
         aspiration="Sequential Twin-Turbo", fuel_type="Petrol", redline=7200,
         transmission_type="6-speed Manual", gear_count=6, drivetrain="RWD",
         units_produced="45200", units_sold="45200", market_availability="Discontinued",
         msrp="$40,000", launch_date="1993-04-01",
         competitors="Nissan Skyline GT-R, Mazda RX-7", awards="JDM Icon",
         historical_importance="The 2JZ legend — 1,000+ hp capable on stock internals.",
         image_url="https://images.unsplash.com/photo-1632245889029-e406faaa34cd?w=1200"),
    dict(brand="Tesla", model="Model S", generation="Plaid", category="Electric",
         production_years="2021–Present", status="Production", country="USA",
         manufacturer="Tesla, Inc.", horsepower=1020, torque=1420, top_speed=322,
         accel_0_100=2.1, quarter_mile=9.23, weight=2162,
         length=4970, width=1964, height=1445, wheelbase=2960,
         engine_name="Tri-Motor Electric", engine_layout="Electric", cylinders=0,
         aspiration="N/A", fuel_type="Electric", transmission_type="Single-speed",
         gear_count=1, drivetrain="AWD", units_produced="100000+", units_sold="100000+",
         market_availability="Global", msrp="$89,990", launch_date="2021-06-10",
         competitors="Lucid Air Sapphire, Porsche Taycan", awards="",
         historical_importance="Fastest-accelerating production sedan at launch.",
         image_url="https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=1200"),
    dict(brand="Porsche", model="911", generation="992 GT3 RS", category="Sports",
         production_years="2022–Present", status="Production", country="Germany",
         manufacturer="Porsche AG", horsepower=525, torque=465, top_speed=296,
         accel_0_100=3.2, quarter_mile=10.9, weight=1450,
         length=4572, width=1900, height=1322, wheelbase=2457,
         engine_name="4.0L Flat-6", engine_code="MDG.G", engine_layout="Boxer 6",
         displacement=4.0, cylinders=6, aspiration="Naturally Aspirated",
         fuel_type="Petrol", redline=9000, transmission_type="7-speed PDK",
         gear_count=7, drivetrain="RWD", units_produced="", units_sold="",
         market_availability="Global", msrp="$241,300", launch_date="2022-08-17",
         competitors="McLaren 765LT", awards="",
         historical_importance="Track-focused 911 with F1-derived aero.",
         image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1200"),
]

ENGINES = [
    dict(name="EcoBoost 1.0 Inline 3", layout="Inline 3", power_hp=125, torque_nm=170, weight_kg=97),
    dict(name="K20C1 Turbo Inline 4", layout="Inline 4", power_hp=320, torque_nm=420, weight_kg=145),
    dict(name="2JZ-GTE Inline 6", layout="Inline 6", power_hp=326, torque_nm=440, weight_kg=230),
    dict(name="Ferrari F154 Twin-Turbo V8", layout="V8", power_hp=710, torque_nm=770, weight_kg=210),
    dict(name="Lamborghini 5.2 V10", layout="V10", power_hp=640, torque_nm=600, weight_kg=235),
    dict(name="Ferrari F140 6.5 V12", layout="V12", power_hp=830, torque_nm=697, weight_kg=256),
    dict(name="Bugatti 8.0 Quad-Turbo W16", layout="W16", power_hp=1500, torque_nm=1600, weight_kg=400),
    dict(name="Porsche 4.0 Boxer 6", layout="Boxer 6", power_hp=525, torque_nm=465, weight_kg=180),
    dict(name="Mazda 13B-REW Rotary", layout="Rotary", power_hp=276, torque_nm=314, weight_kg=122),
    dict(name="Tesla Plaid Tri-Motor", layout="Electric", power_hp=1020, torque_nm=1420, weight_kg=270),
    dict(name="AMG ONE F1 Hybrid", layout="Hybrid System", power_hp=1063, torque_nm=1000, weight_kg=270),
]

MATERIALS = [
    dict(name="Steel", weight_factor=1.00, strength_factor=1.0, description="Traditional automotive steel."),
    dict(name="High Strength Steel", weight_factor=0.85, strength_factor=1.4, description="Modern safety-cell alloys."),
    dict(name="Aluminum", weight_factor=0.55, strength_factor=0.9, description="Lightweight metal (Audi, Tesla)."),
    dict(name="Carbon Fiber", weight_factor=0.30, strength_factor=2.5, description="Motorsport-grade composite."),
    dict(name="Titanium", weight_factor=0.60, strength_factor=2.2, description="Aerospace metal."),
    dict(name="Magnesium", weight_factor=0.40, strength_factor=0.8, description="Ultra-light racing alloy."),
    dict(name="Fiberglass", weight_factor=0.45, strength_factor=0.6, description="Classic Corvette-era composite."),
    dict(name="Kevlar", weight_factor=0.35, strength_factor=1.8, description="Impact-resistant aramid fiber."),
    dict(name="Plastic Composite", weight_factor=0.50, strength_factor=0.5, description="Reinforced polymers."),
    dict(name="Graphene Composite", weight_factor=0.20, strength_factor=3.5, description="Next-gen nanomaterial."),
]

COLORS = [
    ("Rosso Corsa", "#D40000"), ("British Racing Green", "#004225"),
    ("Nardo Gray", "#686A6C"), ("Midnight Black", "#0A0A0A"),
    ("Pearl White", "#F8F6F0"), ("Sapphire Blue", "#0F52BA"),
    ("Arctic Silver", "#C5C9C7"), ("Sunburst Yellow", "#FFC512"),
    ("Candy Red", "#C41E3A"), ("Miami Blue", "#00B7EB"),
    ("Lava Orange", "#F25C19"), ("Guards Red", "#CC0605"),
    ("Gulf Blue", "#7BB2DD"), ("Papaya Orange", "#FF8000"),
    ("Giallo Modena", "#FFD800"), ("Soul Red Crystal", "#8B0000"),
    ("Championship White", "#F4F5F0"), ("Tanzanite Blue", "#1F2A44"),
]


def run():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        for c in CARS:
            car = Car(**c)
            car.gallery = c["image_url"]
            db.session.add(car)
        for e in ENGINES:
            db.session.add(Engine(**e))
        for m in MATERIALS:
            db.session.add(Material(**m))
        for name, hexc in COLORS:
            db.session.add(Color(name=name, hex_code=hexc))
        db.session.commit()
        print("✅ Seeded successfully!")


if __name__ == "__main__":
    run()