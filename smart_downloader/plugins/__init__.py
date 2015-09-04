import importlib
import pkgutil
import os
from celery import current_task

class ProviderClass(object):
    def match_pattern(self, file_url):
        """
        Returns True if the provider can download from that URL
        """
        raise NotImplementedError()

    def find_more_links(self, data=None):
        """
        Returns a list of tuples (File easy name, File URL)
        """
        pass

    def find_title(self, url=None):
        raise NotImplementedError()

    def download(self, url=None, output=None):
        raise NotImplementedError()

    def total_bytes(self, task=None):
        raise NotImplementedError()

    def downloaded_bytes(self, task=None):
        raise NotImplementedError()

    def progress_hook(self, info):
        current_task.update_state(
            state='PROGRESS',
            meta={
                'current': info.get('downloaded_bytes', '0'),
                'total': info.get('total_bytes', '0')
            }
        )

for (module_loader, name, ispkg) in pkgutil.iter_modules(
        [os.path.dirname(__file__)]):
    importlib.import_module('smart_downloader.plugins.' + name, __package__)

all_plugins = []
for kls in ProviderClass.__subclasses__():
    if kls.__name__ != 'DefaultProvider':
        all_plugins.append('.'.join([kls.__module__, kls.__name__]))
all_plugins.append('smart_downloader.plugins.default.DefaultProvider')
