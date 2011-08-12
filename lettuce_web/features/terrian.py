# -*- coding: utf-8 -*-

import os

from lettuce import before, world
from nose.tools import assert_raises


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
        if url == 'test':
            return '/builded-view/'
        return url

    def get_url(self, url, **kwargs):
        """
        Mock GET request with fake html page
        """
        code = 200

        # handle '/redirect' url and
        # show 304 HTTP response code
        if url == '/redirect':
            code = 304

        return {}, code, self.fake_html

    def post_url(self, url, **kwargs):
        """
        Mock POST request with fake HTML page
        """
        code = 200

        if url == '/redirect':
            code = 304

        if 'data' in kwargs:
            self.request_data = kwargs.pop('data')

        return {}, code, self.fake_html


# we use here direct link to absorb.world to avoid
# pyflakes noise. And it's just much clearer for my opinion
absorb.world.webenv_class = DummyEnviron


@before.each_step
def cleanup_attributes(step):
    """
    Shortcut to cleanup last opened page attributes
    from `world`
    """

    try:
        delattr(world, 'response_body')
        delattr(world, 'response_code')
        delattr(world, 'response')
        delattr(world, 'tree')
    except AttributeError:
        pass

    with assert_raises(AttributeError):
        world.response_body
        world.response_code
        world.response
        world.tree
