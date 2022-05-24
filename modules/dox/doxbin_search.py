from pwnmap.module import Module
from pwnmap.util import BoxUtil, DuckDuckGo


class pwnmapModule(Module):
    description = 'Lookup published doxxes from DoxBin site'
    author = 'evan'
    date = '01-01-3030'

    def execute(self, keywords: str):
        results = DuckDuckGo.search(f'site:doxbin.org "{keywords}"')

        if len(results) == 0:
            raise Exception('No results found')

        def __check(keyword, url):
            """ Validate search result """
            if 'doxbin.org/user' in url:
                if not keyword.lower() in url.lower():
                    return False
            return True

        BoxUtil.boxify(
            [
                {'Title': title, 'URL': url}
                for url, title in results
                if __check(keywords, url) is True
            ],
            title='Doxbin results',
            show_keys=True
        )
