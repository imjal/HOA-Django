from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Household, Invoice
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, EmailInvoiceForm, InvoiceForm, HouseholdForm, AgentEmailForm
from django.core.mail import send_mail
from utils.sale_extraction import list_sale, compare2List, send_agent_email

# Create your views here.


def household_list(request):
	homes = Household.objects.all().order_by('last_name1')
	return render(request, 'invoice/household_list.html', {"homes": homes})

def home_page(request):
	#notices = Notice.objects.all()
	return render(request, 'invoice/home_page.html')

def display_form(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			for line in file:
				row = line.decode('utf8').strip().split(',')
				row[8] = row[8].replace("-", '')
				_, created = Household.objects.get_or_create(
					last_name1 = row[0],
					first_name1= row[1],
					last_name2 = row[2],
					first_name2 = row[3],
					address = row[4],
					house_number = int('0' + row[5]),
					street_name = row[6],
					email = row[7],
					phone_number = int('0'+ row[8]),
				)	

			return HttpResponseRedirect('success_upload')
	else:
		form = UploadFileForm()
	return render(request, 'invoice/upload_spreadsheet.html', {'form': form})

def success_upload(request):
	return render(request, 'invoice/success_upload.html')

def invoices(request):
	invoice_objs = Invoice.objects.all()
	return render(request, 'invoice/invoices.html', {"invoices": invoice_objs})

def send_invoice(request):
	if request.method == 'POST':
		form = EmailInvoiceForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['homeowner'] is None:
				all_emails = Household.objects.values_list('email', flat=True)
				#send_mail(form.cleaned_data['subject'], form.cleaned_data['message'], form.cleaned_data['sender_email'], all_emails)
				Invoice.objects.bulk_create([Invoice(homeowner=n, status=form.cleaned_data['status'], amount_pending=form.cleaned_data['amount_pending']) for n in Household.objects.all()])
			else:
				homeowner = form.cleaned_data['homeowner']
				send_mail(form.cleaned_data['subject'], form.cleaned_data['message'], form.cleaned_data['sender_email'], [homeowner.email])
				form.save()
			return redirect('invoices')
	else:
		form = EmailInvoiceForm()
	return render(request, 'invoice/send_invoice.html', {'form': form})

def edit_invoice(request, pk):
	invoice = get_object_or_404(Invoice, pk=pk)
	if request.method == 'POST':
		form = InvoiceForm(request.POST, instance=invoice)
		form.save()
		return redirect('invoices')
	else:
		form = InvoiceForm(instance=invoice)
	return render(request, 'invoice/edit_invoice.html', {'form': form})

def edit_household(request, pk):
	household = get_object_or_404(Household, pk=pk)
	if request.method == 'POST':
		form = HouseholdForm(request.POST, instance=household)
		form.save()
		return redirect('household_list')
	else:
		form = HouseholdForm(instance=household)
	return render(request, 'invoice/edit_household.html', {'form': form})

# try to rethink this process of sending emails via the sale view. 
def sale_list(request):
	sale = list(list_sale().keys())
	sale_homes = Household.objects.filter(address__in=sale).order_by('last_name1')
	sale_homes.update(status = 'SALE')
	email_homes = sale_homes.filter(agent_email_status='NOT SENT')
	dict = {}
	for home in email_homes:
		url = request.build_absolute_uri(reverse('agent_form', args = (home.pk, )))
		dict[home.address] = url
	list_sent = send_agent_email(dict, "Jessica", "Lee", "jesprite14@gmail.com")
	Household.objects.filter(address__in=list_sent).update(agent_email_status='SENT')
	return render(request, 'invoice/sale_list.html', {'homes': sale_homes, 'string': str})




#complete need to somehow embed full url in the agent_email message. 
def agent_form(request, pk):
	household = get_object_or_404(Household, pk=pk)
	if request.method == 'POST':
		form = AgentEmailForm(request.POST, instance=household)
		form.save()
		return redirect('agent_thank_you')
	else:
		form = AgentEmailForm(instance=household)
	return render(request, 'invoice/agent_form.html', {"form": form, "house": household})

def agent_thank_you(request):
	return render(request, 'invoice/agent_thank_you.html')




