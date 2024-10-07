from Travel import db
from abc import abstractmethod
from Travel.metaclasses import ServiceMeta
from Travel.price_descriptor import PriceDescriptor
# Admin model
class Admin(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255), nullable=False)
    password=db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'User("{self.id}","{self.username}")'
    

# Travel service for common methods with abstract method
class TravelService(db.Model,metaclass=ServiceMeta):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    _service_id = db.Column(db.String(50), nullable=False)
    _availability = db.Column(db.Boolean, default=True)
    _price = db.Column(db.Float, nullable=False)
    _service_registry = []  # Global registry for services

    price = PriceDescriptor(min_price=0, max_price=10000)  # Applying PriceDescriptor


    def __init__(self, service_id, price, availability=True):
        self._service_id = service_id
        self._price = price
        self._availability = availability
        if not self.__class__.__abstract__:
            self.__class__._service_registry.append(self)

    @property
    def service_id(self):
        return self._service_id
    
    @service_id.setter
    def service_id(self,value):
        self._service_id=value

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value):
        self._availability = value

    @abstractmethod
    def calculate_cost(self):
        pass

    @classmethod
    def get_total_services(cls):
        return len(cls._service_registry)

    @staticmethod
    def is_valid_service_id(service_id):
        return isinstance(service_id, str) and len(service_id) > 0

    def __str__(self):
        return f"{self.__class__.__name__}(ID: {self._service_id}, Price: {self._price}, Available: {self._availability})"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._service_id}>"

    def __eq__(self, other):
        return isinstance(other, TravelService) and self._service_id == other._service_id


# Flight model by using inheritance
class Flight(TravelService):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    from1 = db.Column(db.String(100), nullable=False)
    to = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    airline = db.Column(db.String(100), nullable=False)

    def __init__(self, service_id, price,from1,to, departure_time, arrival_time, airline, availability=True):
        super().__init__(service_id, price, availability)
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.airline = airline
        self.from1 = from1
        self.to=to

    def calculate_cost(self):
        duration = (self.arrival_time - self.departure_time).total_seconds() / 3600
        cost = self.price * duration * 0.1
        return round(cost,1)
    
    def display(self):
        return (f"Flight - {super().display()}, From: {self.from_city}, To: {self.to_city}, "
                f"Departure: {self.departure_time}, Arrival: {self.arrival_time}")

# Hotel model by using inheritance
class Hotel(TravelService):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    

    def __init__(self, service_id, price, location, name,availability=True):
        super().__init__(service_id, price, availability)
        self.location = location
        self.name = name
        

    def calculate_cost(self):
        return self.price
    
    def display(self):
        return f"Hotel - {super().display()}, Name: {self.name}, Location: {self.location}"

# PackageDeal model by using inheritance
class PackageDeal(db.Model,metaclass=ServiceMeta):
    __tablename__ = 'package_deals'
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.String(50), unique=True, nullable=False)

    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))

    flight = db.relationship('Flight', backref='package_deals')
    hotel = db.relationship('Hotel', backref='package_deals')

    availability = db.Column(db.Boolean, default=True)


    def get_total_price(self):
        flight_cost = self.flight.calculate_cost() if self.flight else 0
        hotel_cost = self.hotel.calculate_cost() if self.hotel else 0
        total = flight_cost + hotel_cost
        # print(f"Flight Cost: {flight_cost}, Hotel Cost: {hotel_cost}, Total Price: {total}")
        return total
    def is_available(self):
        return self.flight.availability and self.hotel.availability


db.create_all()

