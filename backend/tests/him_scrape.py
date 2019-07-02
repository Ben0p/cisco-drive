import bs4 as bs
import requests
import utm
import time


utmnum = 50
utmlet = 'K'
ximinfo = {}
ximlist = {}


def scrape(ip):
    url = ''.join(['http://', ip, ':3785/getinfocore'])

    resp = requests.get(url, timeout=1)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    device = soup.find("td", text='Device ID:').find_next_sibling('td').text
    easting = soup.find("td", text='Easting (m):').find_next_sibling('td').text
    northing = soup.find("td", text='Northing (m):').find_next_sibling('td').text
    elevation = soup.find("td", text='Elevation (m):').find_next_sibling('td').text
    latlon = utm.to_latlon(float(easting),float(northing),utmnum,utmlet)

    ximinfo['device'] = device
    ximinfo['ip'] = ip
    ximinfo['easting'] = easting
    ximinfo['northing'] = northing
    ximinfo['elevation'] = elevation
    ximinfo['latitude'] = latlon[0]
    ximinfo['longitude'] = latlon[1]



if __name__ == '__main__':
    while True:
        scrape('10.221.65.128')
        print(ximinfo)
        time.sleep(1)