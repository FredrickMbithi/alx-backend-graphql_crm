from django.db import models

# Create your models here.



class Customer(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=15)

	def __str__(self):
		return self.name



class Product(models.Model):
	name = models.CharField(max_length=100)
	stock = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.name} (Stock: {self.stock})"

class Order(models.Model):
	customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	# Add other fields as needed

	def __str__(self):
		return f"Order {self.id} for {self.customer.name}"
