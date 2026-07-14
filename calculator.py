"""
CarVerse Performance Calculator.
Works with column names: weight, torque, top_speed (and old style too).
"""


def _get(obj, names, default=0):
    """Try multiple attribute names, return first non-empty value."""
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            if v:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    pass
    return default


def calculate(car, engine=None, material=None):
    base_hp = _get(car, ["horsepower", "power_hp"], 100)
    base_weight = _get(car, ["weight", "weight_kg"], 1400)
    base_top = _get(car, ["top_speed", "top_speed_kmh"], 180)
    base_torque = _get(car, ["torque", "torque_nm"], 200)
    base_accel = _get(car, ["accel_0_100"], 0)
    base_quarter = _get(car, ["quarter_mile"], 0)
    drivetrain = getattr(car, "drivetrain", "RWD") or "RWD"

    # --- Engine swap ---
    hp = _get(engine, ["power_hp", "horsepower"], base_hp) if engine else base_hp
    torque = _get(engine, ["torque_nm", "torque"], base_torque) if engine else base_torque

    weight = base_weight
    if engine:
        stock_engine_w = base_weight * 0.12
        eng_w = _get(engine, ["weight_kg", "weight"], stock_engine_w)
        weight = base_weight - stock_engine_w + eng_w

    # --- Material swap (body ≈ 45% of weight) ---
    if material:
        wf = _get(material, ["weight_factor"], 1.0)
        body_w = weight * 0.45
        weight = weight - body_w + body_w * wf

    weight = max(round(weight), 400)
    ptw = round(hp / weight * 1000, 1)
    base_ptw = round(base_hp / base_weight * 1000, 1)

    top_speed = round(base_top * (hp / base_hp) ** (1 / 3))

    accel = round(max(2.0, 300.0 / ptw + 0.6), 2)
    if accel < 2.3 and drivetrain != "AWD":
        accel = round(accel + 0.4, 2)

    quarter = round(5.825 * (weight / max(hp, 1)) ** (1 / 3) + 3.2, 2)

    return {
        "horsepower": round(hp),
        "torque": round(torque),
        "top_speed": top_speed,
        "accel_0_100": accel,
        "quarter_mile": quarter,
        "weight": weight,
        "power_to_weight": ptw,
        "baseline": {
            "horsepower": round(base_hp),
            "torque": round(base_torque),
            "top_speed": round(base_top),
            "accel_0_100": base_accel,
            "quarter_mile": base_quarter,
            "weight": round(base_weight),
            "power_to_weight": base_ptw,
        },
    }