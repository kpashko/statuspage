from bs4 import BeautifulSoup
import requests
import sys
import re

sys.setrecursionlimit(10000)

ua = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                    ' Chrome/53.0.2785.143 Safari/537.36'}

links = {'npm': 'https://status.npmjs.org', 'pd': 'https://status.pagerduty.com',
         'sfx': 'https://signalfx.statuspage.io', 'redis': 'https://status.redislabs.com',
         'papertrail': 'https://www.papertrailstatus.com', 'github': 'https://www.githubstatus.com',
         'spotinst': 'http://status.spotinst.com', 'tab': 'https://trust.tableau.com',
         'zen': 'https://status.zendesk.com', 'atl': 'https://status.atlassian.com',
         'atl_dev': 'https://developer.status.atlassian.com', 'slack': 'https://status.slack.com',
         'facebook': 'https://www.facebook.com/platform/api-status/', 'google': 'https://status.cloud.google.com',
         'cloudflare': 'https://www.cloudflarestatus.com'}


class Status:
    def __init__(self):
        self.links = links
        self.responses = {}

    def sfx(self):
        site = requests.get(links['sfx'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')  # lxml?
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

    def atlassian(self):
        site = requests.get(links['atl'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "all systems operational" not in r.text.lower():
            self.responses['atl'] = 'Red'
            return
        self.responses['atl'] = 'Green'

    def atlassian_dev(self):
        site = requests.get(links['atl_dev'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "all systems operational" not in r.text.lower():
            self.responses['atl_dev'] = 'Red'
            return
        self.responses['atl_dev'] = 'Green'

    def slack(self):
        site = requests.get(links['slack'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['tiny'])
        for elem in r:
            if 'no issues' not in elem.text.lower():
                self.responses['slack'] = 'Red'
                return
            self.responses['slack'] = "Green"

    def facebook(self):
        site = requests.get(links['facebook'], headers=ua).content.decode()
        if '"health": 1' not in site:
            self.responses['fb'] = 'Red'
            return
        self.responses['fb'] = 'Green'

    def google(self):
        site = requests.get(links['google'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('span', class_="status")
        if "all services available" in r.text.lower():
            self.responses['gcp'] = "Green"
        else:
            self.responses['gcp'] = "Red"

    def cloudflare(self):
        site = requests.get(links['cloudflare'], headers=ua).content
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "all systems operational" not in r.text.lower():
            self.responses['cloudflare'] = 'Red'
            return
        self.responses['cloudflare'] = 'Green'

    def update(self):
        self.sfx()
        self.redis()
        self.papertrail()
        self.pd()
        self.github()
        self.npm()
        self.spotinst()
        self.tableau()
        self.atlassian()
        self.atlassian_dev()
        self.slack()
        self.facebook()
        self.google()
        self.cloudflare()

    def pr(self):
        print(self.responses)


##link = "https://status.aws.amazon.com"
##site = requests.get(link, headers=ua).content
##soup = BeautifulSoup(site, "html.parser")
# r = soup.find_all('td', class_='bb top pad8')
# res = []

# mysite = '<td class="bb top pad04 center" style="width: 32px"><img src="/images/status0.gif"></td> <td class="bb top pad8">Amazon Athena (Oregon)</td> <td class="bb pad8">Service is operating normally</td> <td class="bb center top"><a href="/rss/athena-us-west-2.rss"><img style="margin-top: 8px" src="/images/feed-icon-14x14.png"></a></td>' \
#          '<td class="bb top pad8">Amazon API Gateway (Ohio)</td><td class="bb pad8">Service is operating normally</td><td class="bb top pad8">Amazon Athena (N. Virginia)</td>' \
#          '<td class="bb pad8">Service is operating normally</td>'
#reg = "<td.*?\"bb top pad8\">.*Ohio.|.*N. Virginia.</td><.*\">(.*?)</td>"
##reg_oh = "<td.*?\"bb top pad8\">(.*Ohio|.*N. Virginia.*)</td>"
##res = re.findall(reg_oh, str(soup))
# soup = BeautifulSoup(mysite, 'html.parser')
# r = soup.find_all('td', string=re.compile(r'.*Ohio.|.*N. Virginia.'))
##print(res)
