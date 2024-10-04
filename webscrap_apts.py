import requests
from bs4 import BeautifulSoup
import os # Used for accessing environment variables set using setx commands in Windows.

# For this project, I have chosen 'theblueground' website to search Seattle apartments.
url = "https://www.theblueground.com/furnished-apartments-seattle-usa"

def webscrap_apts(budget):
    # Sites block IP addresses of bots like these so we need Proxy Servers: helps bypassing captchas; can set it to any location.
    # Tech like DataImpulse provide such ready-made proxies.
    # Proxy configuration with login and password
    proxy_host = 'gw.dataimpulse.com'
    proxy_port = 823
    proxy_login = os.getenv('PROXY_LOGIN')
    proxy_password = os.getenv('PROXY_PASSWORD')
    proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

    proxies = {
        'http': proxy,
        'https': proxy
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, proxies= proxies)

    # Parse the webpage in a format to search up things - get the entire html to extract the data we need
    soup = BeautifulSoup(response.text, 'html.parser')
    
    apt_list = soup.find_all('a', class_="property") # Find and list all the "<a> {html tag}" elements with class = "property"
    filtered_apt = []

    for apt in apt_list:
        url_ = apt.get('href')
        # find() used below for finding single HTML tag (<span/> in this case). text.strip() --> removes the entire html syntax and leaves just the text within (i.e. the content/substance which here is the "price").
        price = apt.find('span', class_="price__amount").text.strip()
        listing_title = apt.find('span', class_="property__name").text.strip()
        area = apt.find('span', class_="property__address").text.strip()

        final_url = "https://www.theblueground.com" + url_
        price = float(price.replace(",", ""))
        if price < budget:
            filtered_apt.append((listing_title, area, price, final_url))

    return filtered_apt