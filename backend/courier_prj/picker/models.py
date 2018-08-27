from django.db import models

class TestModel(models.Model):
    string = models.CharField(max_length=10)
    number = models.IntegerField()
