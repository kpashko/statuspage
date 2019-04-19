from bs4 import BeautifulSoup
import sys
import re
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


async def get_npm():
    t = await aiohttp_get(LINKS['npm'])
    soup = BeautifulSoup(t, 'html.parser')
    r = soup.find('span', class_="status font-large").text
    if "operational" not in r.lower():
        RESPONSES['npm'] = 'Red'
        return
    RESPONSES['npm'] = 'Green'


async def get_spot():
    t = await aiohttp_get(LINKS['spotinst'])
    soup = BeautifulSoup(t, 'html.parser')
    r = soup.find('div', class_="section-status").text
    if "operational" not in r.lower():
        RESPONSES['spotinst'] = 'Red'
        return
    RESPONSES['spotinst'] = 'Green'


async def sfx():
    site = await aiohttp_get(LINKS['sfx'])
    soup = BeautifulSoup(site, 'html.parser')  # lxml?
    r = soup.select('rect[class*="day-89"]')
    for elem in r:
        if elem.attrs['fill'] != '#2fcc66':
            RESPONSES['sfx'] = "Red"
            return
    RESPONSES['sfx'] = "Green"


async def redis():
    site = await aiohttp_get(LINKS['redis'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find_all('span', class_='component-status tool')
    for elem in r:
        if "operational" not in elem.text.lower():
            RESPONSES['redis'] = "Red"
            return
    RESPONSES['redis'] = "Green"


async def papertrail():
    site = await aiohttp_get(LINKS['papertrail'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find_all('span', class_='component-status')
    for elem in r:
        if "operational" not in elem.text.lower():
            RESPONSES['papertrail'] = "Red"
            return
    RESPONSES['papertrail'] = "Green"


async def pd():
    site = await aiohttp_get(LINKS['pd'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find_all('span', class_='component-status ')
    for elem in r:
        if "operational" not in elem.text.lower():
            RESPONSES['pd'] = "Red"
            return
    RESPONSES['pd'] = "Green"


async def github():
    site = await aiohttp_get(LINKS['github'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find_all('span', class_='component-status ')
    for elem in r:
        if "operational" not in elem.text.lower():
            RESPONSES['github'] = "Red"
            return
    RESPONSES['github'] = "Green"

"""Tableau will wait for next time"""

# async def tableau():
#     site = await aiohttp_get(LINKS['tab'])
#     soup = BeautifulSoup(site, 'html.parser')
#     r = soup.find('div', class_="page-status")
#     if "operational" not in r.text.lower():
#         RESPONSES['tab'] = 'Red'
#         return
#     RESPONSES['tab'] = 'Green'


async def atlassian():
    site = await aiohttp_get(LINKS['atl'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find('div', class_="page-status")
    if "all systems operational" not in r.text.lower():
        RESPONSES['atl'] = 'Red'
        return
    RESPONSES['atl'] = 'Green'


async def atlassian_dev():
    site = await aiohttp_get(LINKS['atl_dev'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find('div', class_="page-status")
    if "all systems operational" not in r.text.lower():
        RESPONSES['atl_dev'] = 'Red'
        return
    RESPONSES['atl_dev'] = 'Green'


async def slack():
    site = await aiohttp_get(LINKS['slack'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['tiny'])
    for elem in r:
        if 'no issues' not in elem.text.lower():
            RESPONSES['slack'] = 'Red'
            return
        RESPONSES['slack'] = "Green"


"""FB will wait for next time"""
#
# async def facebook():
#     site = requests.get(LINKS['facebook'], headers=ua).content.decode()
#     if '"health": 1' not in site:
#         RESPONSES['fb'] = 'Red'
#         return
#     RESPONSES['fb'] = 'Green'
#


async def google():
    site = await aiohttp_get(LINKS['google'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find('span', class_="status")
    if "all services available" in r.text.lower():
        RESPONSES['gcp'] = "Green"
    else:
        RESPONSES['gcp'] = "Red"


async def cloudflare():
    site = await aiohttp_get(LINKS['cloudflare'])
    soup = BeautifulSoup(site, 'html.parser')
    r = soup.find('div', class_="page-status")
    if "all systems operational" not in r.text.lower():
        RESPONSES['cloudflare'] = 'Red'
        return
    RESPONSES['cloudflare'] = 'Green'


async def main():
    tasks = [get_npm(), get_spot(), cloudflare(), google(), slack(), atlassian_dev(), atlassian(), redis(), sfx(),
             pd(), github(), papertrail()]
    await asyncio.wait(tasks)

asyncio.run(main())
print("final: " + str(RESPONSES))


###########################################################################
# class Status:
#     def __init__(self):
#         self.links = LINKS
#         self.responses = {}
#
#     def sfx(self):
#         site = await aiohttp_get(LINKS['sfx'])
#         site = requests.get(LINKS['sfx'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')  # lxml?
#         r = soup.select('rect[class*="day-89"]')
#
#         for elem in r:
#             if elem.attrs['fill'] != '#2fcc66':
#                 RESPONSES['sfx'] = "Red"
#                 return
#         RESPONSES['sfx'] = "Green"
#
#     def redis(self):
#         site = requests.get(LINKS['redis'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find_all('span', class_='component-status tool')
#         for elem in r:
#             if "operational" not in elem.text.lower():
#                 RESPONSES['redis'] = "Red"
#                 return
#         RESPONSES['redis'] = "Green"
#
#     def papertrail(self):
#         site = requests.get(LINKS['papertrail'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find_all('span', class_='component-status')
#         for elem in r:
#             if "operational" not in elem.text.lower():
#                 RESPONSES['papertrail'] = "Red"
#                 return
#         RESPONSES['papertrail'] = "Green"
#
#     def pd(self):
#         site = requests.get(LINKS['pd'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find_all('span', class_='component-status ')
#         for elem in r:
#             if "operational" not in elem.text.lower():
#                 RESPONSES['pd'] = "Red"
#                 return
#         RESPONSES['pd'] = "Green"
#
#     def github(self):
#         site = requests.get(LINKS['github'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find_all('span', class_='component-status ')
#         for elem in r:
#             if "operational" not in elem.text.lower():
#                 RESPONSES['github'] = "Red"
#                 return
#         RESPONSES['github'] = "Green"
#
#     def npm(self):
#         site = requests.get(LINKS['npm'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('span', class_="status font-large").text
#         if "operational" not in r.lower():
#             RESPONSES['npm'] = 'Red'
#             return
#         RESPONSES['npm'] = 'Green'
#
#     def spotinst(self):
#         site = requests.get(LINKS['spotinst'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('div', class_="section-status").text
#         if "operational" not in r.lower():
#             RESPONSES['spotinst'] = 'Red'
#             return
#         RESPONSES['spotinst'] = 'Green'
#
#     def tableau(self):
#         site = requests.get(LINKS['tab'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('div', class_="page-status")
#         if "operational" not in r.text.lower():
#             RESPONSES['tab'] = 'Red'
#             return
#         RESPONSES['tab'] = 'Green'
#
#     def atlassian(self):
#         site = requests.get(LINKS['atl'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('div', class_="page-status")
#         if "all systems operational" not in r.text.lower():
#             RESPONSES['atl'] = 'Red'
#             return
#         RESPONSES['atl'] = 'Green'
#
#     def atlassian_dev(self):
#         site = requests.get(LINKS['atl_dev'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('div', class_="page-status")
#         if "all systems operational" not in r.text.lower():
#             RESPONSES['atl_dev'] = 'Red'
#             return
#         RESPONSES['atl_dev'] = 'Green'
#
#     def slack(self):
#         site = requests.get(LINKS['slack'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['tiny'])
#         for elem in r:
#             if 'no issues' not in elem.text.lower():
#                 RESPONSES['slack'] = 'Red'
#                 return
#             RESPONSES['slack'] = "Green"
#
#     def facebook(self):
#         site = requests.get(LINKS['facebook'], headers=ua).content.decode()
#         if '"health": 1' not in site:
#             RESPONSES['fb'] = 'Red'
#             return
#         RESPONSES['fb'] = 'Green'
#
#     def google(self):
#         site = requests.get(LINKS['google'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('span', class_="status")
#         if "all services available" in r.text.lower():
#             RESPONSES['gcp'] = "Green"
#         else:
#             RESPONSES['gcp'] = "Red"
#
#     def cloudflare(self):
#         site = requests.get(LINKS['cloudflare'], headers=ua).content
#         soup = BeautifulSoup(site, 'html.parser')
#         r = soup.find('div', class_="page-status")
#         if "all systems operational" not in r.text.lower():
#             RESPONSES['cloudflare'] = 'Red'
#             return
#         RESPONSES['cloudflare'] = 'Green'
#
#     def update(self):
#         self.sfx()
#         self.redis()
#         self.papertrail()
#         self.pd()
#         self.github()
#         self.npm()
#         self.spotinst()
#         self.tableau()
#         self.atlassian()
#         self.atlassian_dev()
#         self.slack()
#         self.facebook()
#         self.google()
#         self.cloudflare()
#
#     def pr(self):
#         print(self.responses)

# method_list = [func for func in dir(Status) if getattr(Status, func)]
#
