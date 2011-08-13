# -*- coding: utf-8 -*-

from flask import url_for
from werkzeug.routing import BuildError

from lettuce_web.environ import LettuceWebTestEnviron


__all__ = ('LettuceFlaskTestEnviron',)


class LettuceFlaskTestEnviron(LettuceWebTestEnviron):
    """
    Very basic driver for Flask. You should initialize
    flask app by yourself and use this class only as
    base class of customized one by you.
    """

    def __init__(self, *args, **kwargs):
        super(LettuceFlaskTestEnviron, self).__init__(*args, **kwargs)

    def build_url(self, url, **kwargs):
        """
        Build url for. This wont work for views
        with keyed arguments therefore I need to handle it
        in future.
        """
        try:
            url = url_for(url)
        except BuildError:
            return url

        return url

    def get_url(self, url, **kwargs):
        """
        Make GET request to the Flask
        """
        response = self.client.get(url, **kwargs)
        response.freeze()

        return response, response.status_code, response.response[0]

    def post_url(self, url, **kwargs):
        """
        Make POST request to the Flask
        """
        response = self.client.post(url, **kwargs)
        response.freeze()
        return response, response.status_code, response.response[0]

    def bootstrap(self):
        """
        Here we need to initialize our Flask App,
        test request context and test client
        """

        # In class inherited from current one
        # after initialization of Flask App and
        # put as `self.app` and
        # `super(Class, self).bootstrap()` should be
        # called to initialize test request context and
        # test client.

        self.client = self.app.test_client()
        self.app.test_request_context().push()

    def destroy(self):
        """
        In this method we'll destroy test request context
        and test client
        """

        self.client = None
        self.app.test_request_context().pop()
