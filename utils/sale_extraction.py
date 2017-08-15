from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from invoice.models import Household, Invoice

"""
	This method grabs information from the site that contains all sale homes in Chadwick Estates. 
	It will select and format the homes on the webpage and display them on our webpage so the Homeowner Associations can keep track of
	the homes on sale. 
	
"""
def list_sale():
	site= "http://markmonge.idxbroker.com/i/ChadwickEstates"
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(site,headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, "lxml")

	all_homes = soup.find_all(class_='IDX-resultsAddress')
	dict = {}
	for home in all_homes:
		house_num = home.select('.IDX-resultsAddressNumber')[0].get_text()
		house_dir = home.select('.IDX-resultsAddressDirection')[0].get_text()
		house_address = home.select('.IDX-resultsAddressName')[0].get_text()
		if("Court" in house_address):
			house_address = house_address.replace("Court", "Ct")		
		house_link = home.select('.IDX-resultsAddressLink')[0].get('href')
		string_format = '{} {}. {} {}.'.format(house_num.replace(" ", ""), house_dir.replace(" ", ""), house_address.split(' ')[0].title(), "".join(list(house_address.split(' ')[1])[0:2]))
		dict[string_format] = house_link
	return dict

"""
	Not sure if this is a necessary method, but we'll see. 
"""
def compare2List(list_home, dict):
	list = []
	print(dict)
	for home in list_home:
		if(dict.get(home.address) is not None):
			list.append(home)
	return list

"""
	Adds url to the message at which the agent can fill out the information. I think I might password protect this part of the site as well. 
"""
def string_edit(url):
	message_str = """
	Hello,
	This is the Chadwick Estates Homeowner’s Association. We are contacting you concerning this current house on the market. Due to the many houses on the market in Peoria, that has resulted in constantly changing homeowners. We ask you to fill out this form: {} when a new homeowner buys this Chadwick Estates home, therefore we can update our database and welcome the new owner to our neighborhood. We appreciate your cooperation.
	Thank you,
	Chadwick Estates Homeowner’s Association
	"""
	return message_str.format(url)

"""
	Send agent a message through the listing site. 
"""
def send_agent_email(dict_home, firstName, lastName, email):
	list_sent = []
	for address in dict_home.keys():
		str = string_edit(dict_home[address])
		print (str)
		hdr = {'User-Agent': 'Mozilla/5.0'}
		payload = {'firstName': firstName, 'lastName': lastName, 'email': email, 'message': str}
		r = requests.post(dict_home[address], data=payload, headers=hdr)
		print(r.status_code)
		if r.status_code != 404:
			list_sent.append(address)
	return list_sent
