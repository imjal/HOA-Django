from django.db import models
from django.utils import timezone

# Create your models here.

class Household(models.Model):
	HOME = (
		('OWNED', 'Owned by Owner'), 
		('SALE', 'On Sale'), 
		('UNKNOWN',"Unknown")
	)

	last_name1 = models.CharField(max_length= 50)
	first_name1 = models.CharField(max_length = 50)
	last_name2 = models.CharField(max_length= 50, null = True, blank=True)
	first_name2 = models.CharField(max_length= 50, null = True, blank = True)
	address = models.CharField(max_length = 50, primary_key=True, unique=True)
	house_number = models.IntegerField()
	street_name = models.CharField(max_length=20)
	email = models.EmailField(max_length= 50)
	phone_number = models.IntegerField()
	status = models.CharField(max_length =10, choices = HOME, default = 'OWNED')
	

	@property
	def full_name(self):
		return self.first_name1 + " " + self.last_name1
	def __str__(self):
		return self.last_name1 + " " + self.address


class Invoice(models.Model):
	homeowner = models.ForeignKey('invoice.Household', related_name='invoices', on_delete= models.CASCADE)
	STAT = (
		('PAID','Paid'),
		('PENDING','Pending'),
		('PAST_DUE','Past Due'),
	)
	status = models.CharField(max_length=10, choices=STAT, default='PENDING')
	date_issued = models.DateField()
	amount_pending = models.DecimalField(max_digits=8, decimal_places = 2)

	def send_invoice(self):
		self.date_issued = timezone.now
		self.save()