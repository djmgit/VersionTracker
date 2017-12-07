import requests
import xml.etree.ElementTree as ET

def get_xml(software):
	term = software + ' vs'
	url = 'http://google.com/complete/search?output=toolbar&q=' + term
	response = requests.get(url)
	return response.text


def xml_to_list(response):
	data = []
	root = ET.fromstring(response)
	csuggestions = root.findall('CompleteSuggestion')
	for cs in csuggestions:
		for suggestion in cs:
			data.append(suggestion.get('data'))
	data = [soft[soft.find('vs') + 2:].strip() for soft in data]
	return data


def get_alternative(soft):
	xml_s = get_xml(soft)
	xml_list = xml_to_list(xml_s)

	return xml_list
