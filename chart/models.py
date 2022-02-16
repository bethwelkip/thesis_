from django.db import models

class Measurements(models.Model):
    time = models.TimeField()
    temp = models.DecimalField(max_digits=3, decimal_places=2)
    co2 = models.DecimalField(max_digits=5, decimal_places=2)
    hum = models.DecimalField(max_digits=2, decimal_places=2)
    



