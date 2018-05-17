from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=254)
    email = models.EmailField()
    reg_date = models.DateTimeField('registration_date')
    last_login_date = models.DateTimeField()

    def __str__(self):

        return self.email