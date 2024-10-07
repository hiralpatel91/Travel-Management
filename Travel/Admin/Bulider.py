from Travel.Admin.models import PackageDeal
import time

# Bulider method to create package by admin
class PackageBuilder:
    def __init__(self):
        self.package = PackageDeal()

    def add_flight(self, flight):
        self.package.flight = flight
        self.package.flight_id = flight.id
        return self

    def add_hotel(self, hotel):
        self.package.hotel = hotel
        self.package.hotel_id = hotel.id
        return self

    def set_package_id(self):
        # Generate a unique package ID using the current timestamp
        self.package.package_id = f"PKG{int(time.time())}"
        return self
    
    def build(self):
        return self.package
