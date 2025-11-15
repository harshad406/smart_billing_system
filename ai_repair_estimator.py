# ai_repair_estimator.py
def estimate_repair_cost(device, issue):
    """
    Very simple model. 
    You can later plug GPT or ML model.
    """
    base_prices = {
        "mobile": 300,
        "laptop": 700,
        "tablet": 400
    }

    issue_factors = {
        "screen": 2.5,
        "battery": 1.8,
        "software": 1.2,
        "water": 3.0,
        "charging": 1.5
    }

    d = device.lower()
    i = issue.lower()

    base = base_prices.get(d, 500)
    factor = issue_factors.get(i, 1.4)

    estimated = base * factor
    return round(estimated, 2)
