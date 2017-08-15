from django import forms
from django.forms import ModelForm
from .models import Invoice, Household

class UploadFileForm(forms.Form):
	file = forms.FileField()


class EmailInvoiceForm(ModelForm):
	sender_email = forms.EmailField()
	subject = forms.CharField(max_length=50)
	message = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Invoice
		fields = ['homeowner', 'status', 'amount_pending']
	

class InvoiceForm(ModelForm):
	class Meta:
		model = Invoice
		fields = ['homeowner', 'status', 'amount_pending']
	
class HouseholdForm(ModelForm):
	class Meta:
		model = Household
		fields = ['last_name1', 'first_name1', 'last_name2', 'first_name2', 'address', 'house_number', 'street_name', 'email', 'phone_number', 'status']

class AgentEmailForm(ModelForm):
	class Meta:
		model = Household
		fields = ['last_name1', 'first_name1', 'last_name2', 'first_name2', 'email', 'phone_number', 'status']
