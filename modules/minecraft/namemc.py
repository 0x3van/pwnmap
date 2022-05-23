import requests
import cfscrape
import bs4

from cumware.module import Module
from cumware.util import PrintUtil


class cumwareModule(Module):
    description = 'Get NameMC profile information by Minecraft username/UUID'
    author = 'evan'
    date = '04-30-2022'

    def execute(self, username: str):
        profile = self.__get_profile(username)

        profile_social_media = profile.get('social_media', {})
        social_media = [[profile_social_media[x], x] for x in profile_social_media] if profile_social_media else []

        PrintUtil.pp({
            'Username'          : profile.get('username'),
            'UUID'              : profile.get('uuid'),
            'Monthly viewers'   : profile.get('monthly_viewers'),
            'Rank'              : profile.get('rank'),
            'Location'          : profile.get('location'),
            'Discord'           : profile.get('discord'),
            'Social media'      : social_media,
            'Profile link'      : profile.get('profile_link'),
        })

    def __get_profile(self, target: str):
        """ Fetch profile information from Minecraft username/UUID """
        class Enums:

            class Title:
                INFORMATION = 'Information'
                CAPES = 'Capes'
                FRIENDS = 'Friends'

            class Status:
                UNAVAILABLE = 'Unavailable'
                INVALID_CHARACTERS = 'Invalid characters'
                TOO_LONG = 'Too long'
                TOO_SHORT = 'Too short'
                AVAILABLE = 'Available*'
                AVAILABLE_LATER = 'Available Later*'
        
        SOCIAL_MEDIA = [
            'GitHub',
            'Reddit',
            'SoundCloud',
            'Telegram',
            'Twitch',
            'Twitter',
            'YouTube'
        ]

        profile_information = {}

        # ??? wont work in italy wtf
        session = requests.session()
        session.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}

        scraper = cfscrape.create_scraper(sess=session)

        res = scraper.get('https://namemc.com/profile/' + target)  # use cfscrape

        if res.status_code != 200:
            if res.status_code == 403:
                raise Exception('Cloudflare error')
            raise Exception('Failed to fetch profile information')

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

       
        username = soup.find('meta', {'name': 'profile:username'})['content']


        profile_link = res.url


        for div_html in soup.find_all('div', {'class': 'col-auto'}):
            if div_html.string:
                if div_html.string.endswith('/ month'):
                    monthly_views = div_html.string.split('/')[0].strip(' ')
                    break
        else:
            monthly_views = -1


        for samp_html in soup.find_all('samp'):
            if samp_html.string:
                if len(samp_html.string) == 32:
                    uuid = samp_html.string
                    break
        else:
            uuid = None

        profile_information |= {'username': username, 'uuid': uuid, 'profile_link': profile_link, 'monthly_viewers': monthly_views}

        for div_html in soup.find_all('div', {'class': 'card mb-3'}):
            title_html = div_html.find('strong')

            if not title_html or not title_html.string:
                continue

            title = title_html.string.strip()

            if title == Enums.Title.INFORMATION:

                rank_html = div_html.find('a', {'class': 'namemc-rank'})
                rank = rank_html.string.strip() if rank_html else None

                for div_html_1 in div_html.find_all('div', {'class': 'col-auto'}):
                    if div_html_1.find('img') is not None:
                        location = div_html_1.text if div_html_1 is not None else None
                        break
                else:
                    location = None

   
                discord_html = div_html.find('a', {'title': 'Discord'})
                discord = discord_html.get('data-content') if discord_html is not None else None

                profile_information |= {'rank': rank, 'location': location, 'discord': discord, 'social_media': {}}

                for social_media_name in SOCIAL_MEDIA:
                    social_media_elem = div_html.find('a', {'title': social_media_name})

                    if social_media_elem:
                        social_media_profile = social_media_elem.get('href').split('?')[0]

                        profile_information['social_media'] |= {social_media_name.lower(): social_media_profile}

        return profile_information
