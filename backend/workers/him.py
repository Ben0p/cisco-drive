import bs4 as bs
import requests
import utm
import time




def scrape(q, ip):
    utmnum = 50
    utmlet = 'K'
    url = ''.join(['http://', ip, ':3785/getinfocore'])


    ximinfo = { }






    while True:

        try:
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
            ximinfo['response'] = True

        except:
            ximinfo['device'] = ''
            ximinfo['ip'] = ip
            ximinfo['easting'] = ''
            ximinfo['northing'] = ''
            ximinfo['elevation'] = ''
            ximinfo['latitude'] = ''
            ximinfo['longitude'] = ''
            ximinfo['response'] = False

        q.put({'him' : ximinfo})
        time.sleep(1)



if __name__ == '__main__':
    import multiprocessing

    ip = '10.221.69.53'
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=scrape, args=(q, ip, ))
    p.start()

    while True:
        line = q.get()
        print(line)


# python ./backend/workers/him.py       