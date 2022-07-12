import cfscrape
import bs4

from pwnmap.module import Module
from pwnmap.util import PrintUtil, HTMLUtil


class pwnmapModule(Module):
    description = 'Get social media profiles on solo.to by username'
    author = 'cs'
    date = '28-07-2021'

    def execute(self, username: str):
        scraper = cfscrape.create_scraper()
        res = scraper.get('https://solo.to/' + username)

        if res.status_code == 404:
            raise Exception('Profile not found')

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        displayed_name = HTMLUtil.get_element_string(
            soup, 
            ('h1', {'class': 'profile-name'})
        )
        location = HTMLUtil.get_element_string(
            soup,
            ('div', {'class': 'profile-location-text'})
        )
        bio = HTMLUtil.get_element_string(
            soup,
            ('p', {'class': 'profile-bio'})
        )

        email, phone = None, None

        for c in soup.find_all('a', 'contact-button w-inline-block'):
            c = c['href']
            c = c[(c.find(':') + 1 if c.find(':') > 0 else 0):]

            if '@' in c:
                email = c
            else:
                phone = c

        links = []

        for link in soup.find_all('div', {'class': 'link-item-wrapper'}):
            url = link.find('a')['href']
            name = link.find('div', {'class': 'link-name'}).text

            links.append([url, name])

        PrintUtil.pp({
            'Display name'  : displayed_name,
            'Location'      : location,
            'Bio'           : bio,
            'Contact email' : email,
            'Contact phone' : phone,
            'Links'         : links
        })