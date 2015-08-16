import importlib
import pkgutil
import os


class ProviderClass(object):
    def match_pattern(self, file_url):
        raise NotImplementedError()

    def find_more_links(self):
        pass

    def download(self):
        raise NotImplementedError()

    def total_bytes(self):
        raise NotImplementedError()

    def downloaded_bytes(self):
        raise NotImplementedError()


for (module_loader, name, ispkg) in pkgutil.iter_modules(
        [os.path.dirname(__file__)]):
    importlib.import_module('smart_downloader.plugins.' + name, __package__)

__all_plugins__ = ['.'.join([x.__module__, x.__name__]) for x in
                   ProviderClass.__subclasses__()]
