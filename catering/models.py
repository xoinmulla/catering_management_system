from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)  # E.g., Wedding, Birthday

class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Order(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu)
    order_date = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
class Staff(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)  # e.g., Chef, Server, Coordinator
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
