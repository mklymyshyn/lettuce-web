from lxml import html


__all__ = ('LettuceWebTestEnviron',)


class LettuceWebTestEnviron(object):
    """
    Abstract class to create concrete framework implementation
    """

    def __init__(self, world):
        self.world = world

    def bootstrap(self):
        """
        Abstract method to bootstrap test environment
        before all scenarios
        """

        pass

    def build_url(self, url):
        """
        Method to build urls with tools from particular framework
        """
        raise NotImplementedError(u"This method should be implemented "\
                                  u"to build urls to the views")

    def destroy(self):
        """
        Abstract method to destroy test environment
        after all scenarios
        """

        pass

    def get_url(self, **kwargs):
        """
        Abstract method to fetch url and receive response

        This method should be overriden by concrete framework
        environment implementation
        """

        raise NotImplementedError("Please, implement GET url functionality")

    def pre_process_response(self, response_body, response, tree=False):
        """
        This method may be overriden in concrete framework
        environment implementation to preprocess raw response
        before parsing by LXML
        """
        return response_body

    def post_process_response(self, response_body, lxml_tree, response):
        """
        Thid method may be overriden to customize LXML tree or
        post-process response
        """

        return response_body, lxml_tree

    def post_url(self, data={}, **kwargs):
        """
        Abstract method to send POST request and receive response.

        This method should be overriden by concrete framework
        environment implementation.
        """

        raise NotImplementedError("Please, implement POST url functionality")

    def url(self, url='/', post=False, tree=False, **kwargs):
        """
        Abstract method to open url, make POST request, parse
        LXML tree and so on

        if tree == True then to the worl LXML tree parsed value
        will be added.

        LXML tree available in `world` as `tree` attribute,
        current view url (built by `build_url` method) will be
        passed to the `world` as `current_url` attribute

        Usage:
            world.env.url(url='<view>')
            world.env.url(url='/hardcoded/url/')
            world.env.url(url='<view>', post=True, data={
            'var1': 'val1',
            'var2': 'val2',
            })
        """

        lxml_tree = None

        request_method = {
        True: 'post',
        False: 'get',
        }

        url = self.build_url(url)

        self.world.current_url = url
        self.world.tree = None

        url_func = getattr(self, '%s_url' % request_method[post])
        response, code, response_body = url_func(url, **kwargs)

        # pre-process response
        response_body = self.pre_process_response(response_body, response,
                                                  tree=tree)

        if tree:
            # todo parse with lxml
            lxml_tree = html.fromstring(response_body)

        # post-process response
        response_body, lxml_tree = self.post_process_response(response_body,
                                                              lxml_tree,
                                                              response)

        self.world.tree = lxml_tree

        return response, code, response_body

    def set_up(self):
        """This one only for overriding"""
        pass

    def tear_down(self):
        """Method only for overriding"""
        pass
