import requests

from smart_downloader.plugins import ProviderClass


class A3Media(ProviderClass):
    def find_more_links(self):
        response = requests.get(self.provider_url + 'carousel.json')
        for element in response.json()['1']:
            return [
                ('Retorno a Lilifor ' + element['title'], element['hrefHtml'])]
