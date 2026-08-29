from .models import CarMake, CarModel


CAR_CATALOG = {
    "Audi": [("A4", "Sedan", 2022), ("Q5", "SUV", 2023)],
    "BMW": [("330i", "Sedan", 2021), ("X5", "SUV", 2023)],
    "Chevrolet": [("Malibu", "Sedan", 2022), ("Tahoe", "SUV", 2023)],
    "Ford": [("Mustang", "Coupe", 2022), ("F-150", "Truck", 2023)],
    "Honda": [("Accord", "Sedan", 2022), ("CR-V", "SUV", 2023)],
    "Hyundai": [("Elantra", "Sedan", 2022), ("Tucson", "SUV", 2023)],
    "Kia": [("K5", "Sedan", 2022), ("Sportage", "SUV", 2023)],
    "Mercedes-Benz": [("C-Class", "Sedan", 2022), ("GLC", "SUV", 2023)],
    "Nissan": [("Altima", "Sedan", 2022), ("Rogue", "SUV", 2023)],
    "Toyota": [("Camry", "Sedan", 2022), ("RAV4", "SUV", 2023)],
}


def initiate() -> None:
    for make_name, model_rows in CAR_CATALOG.items():
        make, _ = CarMake.objects.get_or_create(
            name=make_name,
            defaults={"description": f"Popular {make_name} vehicles."},
        )
        for model_name, car_type, year in model_rows:
            CarModel.objects.get_or_create(
                car_make=make,
                name=model_name,
                year=year,
                defaults={"type": car_type},
            )
