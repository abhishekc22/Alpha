from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.


def validate_expiry_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
            (f"Expiry date cannot be earlier than {min_date}.")
        )  
    
def validate_end_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
            (f"End date cannot be earlier than {min_date}.")
        )


class Offer(models.Model):
    name = models.CharField(max_length=50,unique=True)
    off_percent = models.PositiveIntegerField()
    start_date = models.DateField(validators=[validate_expiry_date])
    end_date = models.DateField(validators=[validate_end_date])



    def __str__(self):
        return self.name   
    
    def is_expired(self):
        return date.today() > self.end_date
    
