import collections

from website.yaml_file import YamlFile
import glob
from os import path


class AchievementTranslations:
    def __init__(self):
        self.data = {}

        translations = glob.glob('content/achievements/*.yaml')
        for trans_file in translations:
            lang = path.splitext(path.basename(trans_file))[0]
            self.data[lang] = YamlFile.for_file(trans_file)

    def get_translations(self, language):
        d = collections.defaultdict(lambda: 'Unknown Exception')
        d.update(**self.data.get('en', {}))
        d.update(**self.data.get(language, {}))
        return d


class PageTranslations:
    def __init__(self, page):
        self.data = {}
        if page in ['start', 'join', 'learn-more', 'for-teachers']:
            translations = glob.glob('content/pages/*.yaml')
        else:
            translations = glob.glob('content/pages/' + page + '/*.yaml')
        for file in translations:
            lang = path.splitext(path.basename(file))[0]
            self.data[lang] = YamlFile.for_file(file)

    def exists(self):
        """Whether or not any content was found for this page."""
        return len(self.data) > 0

    def get_page_translations(self, language):
        d = collections.defaultdict(lambda: '')
        d.update(**self.data.get('en', {}))
        d.update(**self.data.get(language, {}))
        return d
