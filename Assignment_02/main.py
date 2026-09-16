from rental import Vehicle, Renter, ElectricCar, Motorbike

def main():
    car = Vehicle("Toyota", "Corolla", "BKK1234")
    ev = ElectricCar("Tesla", "Model Y", "EV5678", 75)
    bike = Motorbike("Yamaha", "R15", "MB8901", 155)

    renter1 = Renter("Hubert", 6705140038)
    renter2 = Renter("Olary", 6705140040)

    print(car)
    car.rent()
    print("Hubert rented car:", car)
    car.return_vehicle()
    print("Car returned:", car)

    try:
        Renter("", 123)
    except ValueError as e:
        print("Caught error:", e)

    try:
        Renter("BadGuy", -5)
    except ValueError as e:
        print("Caught error:", e)

    for v in [car, ev, bike]:
        print(v)

    print(renter1.name, renter1.license_no)
    print(renter2.name, renter2.license_no)

if __name__ == "__main__":
    main()
