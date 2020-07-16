from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class Institution(models.Model):
    name = models.CharField(max_length=248)
    description = models.TextField()
    types = [
        (1, 'Foundation'),
        (2, 'Non-governmental organization'),
        (3, 'Local collection')
    ]
    type = models.IntegerField(choices=types, default=1)
    categories = models.ManyToManyField(Category)


def quantity_validation(value):
    if value < 0:
        raise ValidationError("The quantity cannot be negative!")

def zip_code_validation(code):
    if code != r'\d{2}-\d{3}':
        raise ValidationError("The value is not a valid zipcode in Poland")


# zip_code_regex = RegexValidator(regex=r'\d{2}-\d{3}', message="The value is not a valid zipcode in Poland")
# zip_code = models.CharField(validators=[zip_code_regex])

class Donation(models.Model):
    quantity = models.IntegerField(validators=[quantity_validation])
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(validators=[zip_code_validation], max_length=6)
    pick_up_data = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

