class Vehicle:
    def __init__(self, make, model, plate):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = False

    def rent(self):
        self.is_rented = True

    def return_vehicle(self):
        self.is_rented = False

    def __str__(self):
        status = "rented" if self.is_rented else "available"
        return f"{self.make} {self.model} ({self.plate}) [{status}]"


class Renter:
    def __init__(self, name, license_no):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if license_no <= 0:
            raise ValueError("License number must be positive")
        self._name = name
        self._license_no = license_no
        self.rented = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def license_no(self):
        return self._license_no

    @license_no.setter
    def license_no(self, value):
        if value <= 0:
            raise ValueError("License number must be positive")
        self._license_no = value


class ElectricCar(Vehicle):
    def __init__(self, make, model, plate, battery_kwh):
        super().__init__(make, model, plate)
        self.battery_kwh = battery_kwh

    def __str__(self):
        status = "rented" if self.is_rented else "available"
        return f"{self.make} {self.model} ({self.plate}) {self.battery_kwh}kWh [{status}]"


class Motorbike(Vehicle):
    def __init__(self, make, model, plate, engine_cc):
        super().__init__(make, model, plate)
        self.engine_cc = engine_cc

    def __str__(self):
        status = "rented" if self.is_rented else "available"
        return f"{self.make} {self.model} ({self.plate}) {self.engine_cc}cc [{status}]"
