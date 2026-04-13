def calculate_shipping_cost(weight_kg: float, is_premium: bool) -> float:
    """Calculates the shipping cost based on weight and premium status.

    Args:
        weight_kg: The weight of the package in kilograms.
        is_premium: A boolean indicating if the user has a premium membership.

    Returns:
        The calculated shipping cost.
    """
    base_cost = 5.0
    cost_per_kg = 2.0
    shipping_cost = base_cost + (weight_kg * cost_per_kg)
    if is_premium:
        shipping_cost *= 0.9  # Apply a 10% discount for premium members
    return shipping_cost




