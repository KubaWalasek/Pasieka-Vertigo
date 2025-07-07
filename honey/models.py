from django.db import models

class HoneyTaste(models.Model):
    HONEY_TASTE_CHOICES = [
        ('Akacja', 'Akacjowy'),
        ('Rzepak', 'Rzepakowy'),
        ('Spadź', 'Spadziowy'),
        ('Facelia', 'Faceliowy'),
        ('Gryka', 'Gryczany'),
        ('Lipa', 'Lipowy'),
        ('Malina', 'Malinowy'),
        ('Imbir', 'Imbir z cytryną'),
        ('Żurawina', 'Żurawinowy'),
        ('Porzeczka', 'Porzeczkowy')
    ]
    taste = models.CharField(max_length=50, choices=HONEY_TASTE_CHOICES, default='Akacja')

    def __str__(self):
        return f'{self.get_taste_display()}'

class HoneyType(models.Model):
    HONEY_TYPE_CHOICES = [
        ('kremowany', 'Kremowany'),
        ('naturalny', 'Naturalny'),
        ('smak', 'Smakowy')
    ]
    type = models.CharField(max_length=50, choices=HONEY_TYPE_CHOICES, default='naturalny')

    def __str__(self):
        return f'{self.get_type_display()}'

class HoneyVariant(models.Model):
    HONEY_VARIANT_CHOICES = [
        ('50', 'Small - 50ml'),
        ('400', 'Medium - 400ml'),
        ('1000', 'Large - 1000ml')
    ]
    variant = models.CharField(max_length=50, choices=HONEY_VARIANT_CHOICES, default='1000')

    def __str__(self):
        return f'{self.get_variant_display()}'

# tworzymy ofertę z pojedynczych elementow jeden smak, jedna wielkosc ,itp.
class HoneyOffer(models.Model):
    taste = models.ForeignKey(HoneyTaste, on_delete=models.CASCADE, default=1)
    type = models.ForeignKey(HoneyType, on_delete=models.CASCADE, default=1)
    variant = models.ForeignKey(HoneyVariant, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.taste} | {self.type} | {self.variant} | {self.price} zł (ilosc: {self.quantity})'