from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(max_length=200, primary_key=True, auto_created=True, default=uuid.uuid4)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField()
    status = models.BooleanField()
    total_refund = models.PositiveIntegerField()

    def __str__(self):
        return self.username
    
class Items(models.Model):
    id = models.UUIDField(max_length=200, primary_key=True, auto_created=True, default=uuid.uuid4)
    image = models.CharField(max_length=200)
    name = models.TextField()
    price = models.CharField()
    merchant_id = models.UUIDField()

    def __str__(self):
        return self.name
    
class Refund(models.Model):
    id = models.UUIDField(max_length=200, primary_key=True, auto_created=True, default=uuid.uuid4)
    main = models.CharField()
    review = models.CharField()
    caption = models.TextField()
    user = models.CharField()
    item_id = models.UUIDField()
    merchant = models.CharField()
    verdict = models.CharField()
    status = models.BooleanField()