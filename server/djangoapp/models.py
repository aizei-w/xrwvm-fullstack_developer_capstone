from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    COUPE = "Coupe"
    HATCHBACK = "Hatchback"
    TRUCK = "Truck"

    CAR_TYPES = [
        (SEDAN, SEDAN),
        (SUV, SUV),
        (WAGON, WAGON),
        (COUPE, COUPE),
        (HATCHBACK, HATCHBACK),
        (TRUCK, TRUCK),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2026)])

    class Meta:
        ordering = ["car_make__name", "name", "-year"]
        constraints = [models.UniqueConstraint(fields=["car_make", "name", "year"], name="unique_car_model_year")]

    def __str__(self) -> str:
        return f"{self.car_make.name} {self.name} ({self.year})"
