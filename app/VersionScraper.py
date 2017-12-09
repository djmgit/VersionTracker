import requests
from bs4 import BeautifulSoup as bs
import traceback

BASE_URL = "https://filehippo.com/"
END_URL = "history/"

def get_html_page(soft_name, page_no=""):
    URL = BASE_URL + "download_" + soft_name + "/" + END_URL + page_no
    print ("URL : {}".format(URL))
    response = requests.get(URL)
    print ("status code : {}".format(response.status_code))
    return response.text, response.status_code
    #print (reponse.text)

def get_versions(soft_name):
    versions = []
    response = {}
    dates = []

    html, status_code = get_html_page(soft_name)
    if status_code != 200:
        print ('Not found')
        response['found'] = "NOT_FOUND"
        return response
    soup = bs(html, 'html.parser')

    try:
        while True:
            for ver in soup.findAll('a', {'class': 'history-list-font-fix'}):
                print (ver.get_text())
                print (list(ver.next_siblings)[1].get_text())
                versions.append(ver.get_text())
                dates.append(list(ver.next_siblings)[1].get_text())
            next_page = soup.findAll('a', {'class': 'pager-next-link'})
            print (len(next_page))
            if len(next_page) == 0:
                break
            next_page_url = next_page[0].get('href')
            html, status_code = get_html_page(soft_name, next_page_url.split('/')[-2])
            soup = bs(html, 'html.parser')
    
        response['number_of_versions'] = len(versions)
        response['initial_release'] = dates[-1]
        response['versions'] = versions
        response['found'] = "FOUND"
    except:
        traceback.print_exc()
        response['found'] = "NOT_FOUND"

    return response


