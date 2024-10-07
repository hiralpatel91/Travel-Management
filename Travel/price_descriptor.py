class PriceDescriptor:
    def __init__(self, min_price=0, max_price=10000):
        self.min_price = min_price
        self.max_price = max_price

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._price

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a numeric value.")
        if value < self.min_price:
            raise ValueError(f"Price must be at least {self.min_price}.")
        if value > self.max_price:
            raise ValueError(f"Price must not exceed {self.max_price}.")
        instance._price = value

    def __delete__(self, instance):
        raise AttributeError("Price cannot be deleted.")
