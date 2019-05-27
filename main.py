from bs4 import BeautifulSoup
import sys
import asyncio
import aiohttp

RESPONSES = {}

sys.setrecursionlimit(10000)

ua = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                    ' Chrome/53.0.2785.143 Safari/537.36'}

LINKS = {'npm': 'https://status.npmjs.org', 'pd': 'https://status.pagerduty.com',
         'sfx': 'https://signalfx.statuspage.io', 'redis': 'https://status.redislabs.com',
         'papertrail': 'https://www.papertrailstatus.com', 'github': 'https://www.githubstatus.com',
         'spotinst': 'http://status.spotinst.com', 'tab': 'https://trust.tableau.com',
         'zen': 'https://status.zendesk.com', 'atl': 'https://status.atlassian.com',
         'atl_dev': 'https://developer.status.atlassian.com', 'slack': 'https://status.slack.com',
         'facebook': 'https://www.facebook.com/platform/api-status/', 'google': 'https://status.cloud.google.com',
         'cloudflare': 'https://www.cloudflarestatus.com'}


async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def aiohttp_get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


class Status:
    def __init__(self):
        self.links = LINKS
        self.responses = {}

    async def get_npm(self):
        t = await aiohttp_get(LINKS['npm'])
        soup = BeautifulSoup(t, 'html.parser')
        r = soup.find('a', class_="actual-title with-ellipsis").text
        if "operational" not in r.lower():
            self.responses['npm'] = 'Red'
            return
        self.responses['npm'] = 'Green'

    async def get_spot(self):
        t = await aiohttp_get(LINKS['spotinst'])
        soup = BeautifulSoup(t, 'html.parser')
        r = soup.find('div', class_="section-status").text
        if "operational" not in r.lower():
            self.responses['spotinst'] = 'Red'
            return
        self.responses['spotinst'] = 'Green'

    async def sfx(self):
        site = await aiohttp_get(LINKS['sfx'])
        soup = BeautifulSoup(site, 'html.parser')  # lxml?
        r = soup.select('rect[class*="day-89"]')
        for elem in r:
            if elem.attrs['fill'] != '#2fcc66':
                self.responses['sfx'] = "Red"
                return
        self.responses['sfx'] = "Green"

    async def redis(self):
        site = await aiohttp_get(LINKS['redis'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status tool')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['redis'] = "Red"
                return
        self.responses['redis'] = "Green"

    async def papertrail(self):
        site = await aiohttp_get(LINKS['papertrail'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['papertrail'] = "Red"
                return
        self.responses['papertrail'] = "Green"

    async def pd(self):
        site = await aiohttp_get(LINKS['pd'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status ')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['pd'] = "Red"
                return
        self.responses['pd'] = "Green"

    async def github(self):
        site = await aiohttp_get(LINKS['github'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all('span', class_='component-status ')
        for elem in r:
            if "operational" not in elem.text.lower():
                self.responses['github'] = "Red"
                return
        self.responses['github'] = "Green"

    """Tableau will wait for next time"""

    async def tableau(self):
        site = await aiohttp_get(LINKS['tab'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "operational" not in r.text.lower():
            self.responses['tab'] = 'Red'
            return
        self.responses['tab'] = 'Green'

    async def atlassian(self):
        site = await aiohttp_get(LINKS['atl'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "all systems operational" not in r.text.lower():
            self.responses['atl'] = 'Red'
            return
        self.responses['atl'] = 'Green'

    async def atlassian_dev(self):
        site = await aiohttp_get(LINKS['atl_dev'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status")
        if "all systems operational" not in r.text.lower():
            self.responses['atl_dev'] = 'Red'
            return
        self.responses['atl_dev'] = 'Green'

    async def slack(self):
        site = await aiohttp_get(LINKS['slack'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['tiny'])
        for elem in r:
            if 'no issues' not in elem.text.lower():
                self.responses['slack'] = 'Red'
                return
            self.responses['slack'] = "Green"

    async def facebook(self):
        site = await aiohttp_get_json(LINKS['facebook'])
        print(site['current']['health'])
        if site['current']['health'] == 1:
            self.responses['fb'] = 'Green'
            return
        self.responses['fb'] = 'Red'

    async def google(self):
        site = await aiohttp_get(LINKS['google'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('span', class_="status")
        if "all services available" in r.text.lower():
            self.responses['gcp'] = "Green"
        else:
            self.responses['gcp'] = "Red"

    async def cloudflare(self):
        site = await aiohttp_get(LINKS['cloudflare'])
        soup = BeautifulSoup(site, 'html.parser')
        r = soup.find('div', class_="page-status") #add dropdown with text
        if "all systems operational" not in r.text.lower():
            self.responses['cloudflare'] = 'Red'
            return
        self.responses['cloudflare'] = 'Green'

    async def upd(self):
        tasks = [self.get_npm(), self.get_spot(), self.cloudflare(), self.google(), self.slack(), self.atlassian_dev(),
                 self.atlassian(), self.redis(), self.sfx(), self.pd(), self.github(), self.papertrail(),
                 self.tableau(), self.facebook()]
        await asyncio.wait(tasks)



