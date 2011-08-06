import os

from lettuce_web.environ import LettuceWebTestEnviron
from lettuce_web import absorb


class DummyEnviron(LettuceWebTestEnviron):
    def __init__(self, *args, **kwargs):
        dir_path = os.path.abspath(os.path.dirname(__file__))
        self.fake_html = open(os.path.join(dir_path, 'data/index.html')).read()

        super(DummyEnviron, self).__init__(*args, **kwargs)

    def build_url(self, url):
        """
        Just return originally requested url
        """
        return url

    def get_url(self, *kwargs):
        """
        Mock GET request with fake html page
        """
        return {}, 200, self.fake_html

    def post_url(self, **kwargs):
        """
        Mock POST request with fake HTML page
        """
        return {}, 200, self.fake_html


# we use here direct link to absorb.world to avoid
# pyflakes noise. And it's just much clearer for my opinion
absorb.world.webenv_class = DummyEnviron
