from bs4 import BeautifulSoup
import requests
import sys


sys.setrecursionlimit(10000)

ua = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                    ' Chrome/53.0.2785.143 Safari/537.36'}



links = {'npm': 'https://status.npmjs.org', 'pd': 'https://status.pagerduty.com',
         'sfx': 'https://signalfx.statuspage.io', 'redis': 'https://status.redislabs.com',
         'papertrail': 'https://www.papertrailstatus.com', "pd":"https://status.pagerduty.com",
         'github': 'https://www.githubstatus.com', 'npm': 'https://status.npmjs.org',
         'spotinst': 'http://status.spotinst.com', 'tab': 'https://trust.tableau.com',
         'zen':'https://status.zendesk.com'}


class Status:
    def __init__(self):
        self.links = links
        self.responses = {}

    def sfx(self):
        site = requests.get(links['sfx'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser') #lxml?
        r = soup.select('rect[class*="day-89"]')

        for elem in r:
            if elem.attrs['fill'] != '#2fcc66':
                self.responses['sfx'] = "Red"
                return
        self.responses['sfx'] = "Green"

    def redis(self):
        site = requests.get(links['redis'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status tool')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['redis'] = "Red"
                return
        self.responses['redis'] = "Green"

    def papertrail(self):
        site = requests.get(links['papertrail'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['papertrail'] = "Red"
                return
        self.responses['papertrail'] = "Green"

    def pd(self):
        site = requests.get(links['pd'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status ')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['pd'] = "Red"
                return
        self.responses['pd'] = "Green"

    def github(self):
        site = requests.get(links['github'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status ')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['github'] = "Red"
                return
        self.responses['github'] = "Green"

    def npm(self):
        site = requests.get(links['npm'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('span', class_="status font-large").text
        if "operational" not in r.lower():
            self.responses['npm'] = 'Red'
            return
        self.responses['npm'] = 'Green'

    def spotinst(self):
        site = requests.get(links['spotinst'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="section-status").text
        if "operational" not in r.lower():
            self.responses['spotinst'] = 'Red'
            return
        self.responses['spotinst'] = 'Green'

    def tableau(self):
        site = requests.get(links['tab'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "operational" not in r.text.lower():
            self.responses['tab'] = 'Red'
            return
        self.responses['tab'] = 'Green'

    def update(self):
        self.sfx()
        self.redis()
        self.papertrail()
        self.pd()
        self.github()
        self.npm()
        self.spotinst()
        self.tableau()

    def pr(self):
        print(self.responses)


