from django.db import models


class Honey(models.Model):
    HONEY_TYPE_CHOICES = [
        ('Akacja', 'Akacjowy'),
        ('Rzepak', 'Rzepakowy'),
        ('Spadź', 'Spadziowy'),
        ('Facelia', 'Faceliowy'),
        ('Malina', 'Malinowy'),
        ('Imbir', 'Imbir z cytryną'),
        ('Kremowany', 'Kremowany')
    ]

    HONEY_SIZE_CHOICES = [
        ('50', 'Small - 50ml'),
        ('500', 'Medium - 400ml'),
        ('1000', 'Large - 1000ml')
    ]

    type = models.CharField(max_length=50, choices=HONEY_TYPE_CHOICES)
    size = models.CharField(max_length=50, choices=HONEY_SIZE_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)

def __str__(self):
        return f'{self.type} {self.size}'




