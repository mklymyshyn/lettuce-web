# -*- coding: utf-8 -*-

import re

from lettuce import step, world


__all__ = ('open_url', 'assert_link', 'assert_contains',
           'assert_response_code')


@step(u"I go to the \"(.*)\" view(.*)")
def open_url(step, url, skip_tree):
    """
    Generic step to open URL of the site.
    LXML Tree may be generated from response.

    This step will provide to `world` a bunch of useful stuff:
        - current_view -- view name
        - response -- freezed response object
        - content -- HTML content from response

    Also `env.url` add to `world` instance of `lxml.html`
    as `tree` attribute.

    You can skip lxml tree generation by using
    'skip tree' sentence.

    Usage examples:
        I go to the "home" view
        I go to the "/" view
        I go to the "profile" view without tree

    """

    tree = True
    if u'without tree' in skip_tree:
        tree = False

    world.current_view = url

    world.response, \
    world.response_code, \
    world.response_body = world.env.url(url=url, tree=tree)


@step(u"Should(.*) be link to \"(.*)\" view")
def assert_link(step, invert_text, view):
    """
    Check that link to provided view exist on the page.

    This feature make life easy if different views should be available
    for different users (role-based permissions)

    Usage examples:
        Should be link to "/" view
        Shouldn't be link to "/test" view
        Should not be link to "/home" view
    """

    invert = False
    if invert_text in [u'n\'t', u' not']:
        invert = True

    content, tree = world.response_body, world.tree

    url = world.env.get_url(view)

    # find links and set `links` flag respectively to True/False
    links = bool([link for link in tree.iterlinks() if url in link[2]])

    assert_mode = {
        False: links is True,
        True: links is False,
    }

    assert_message = {
        False: u"not exist",
        True: u"exist",
    }

    assert assert_mode[invert], \
        u"Link to the view '%s' *%s* on the page" % (
                                view, assert_message[invert])


@step(u"Page body (.*)contain \"(.*)\"(.*)")
def assert_contains(step, not_contains, text, count):
    """
    Generic shortcut to check that page body
    contain or not contain specified text.
    Example sentences:
      Page body contain "sample text"
      Page body not contain "sample text"
      Page body contain "sample text", exactly 2 times
    """

    is_inverted = u'not' in not_contains

    try:
        count = int(re.match(r'.*exactly\s+(\d+)\s+times',
                    count).group(1))
    except (AttributeError, ValueError):
        count = None

    content = world.response_body

    checks = {
        False: text in content,
        True: text not in content,
    }

    messages = {
        False: u"not ",
        True: u""
    }

    if not checks[is_inverted]:
        assert False, u"Page body %scontain "\
                      u"text \"%s\"" % (messages[is_inverted], text)

    if not count is None:
        # check how exactly times match
        actual_count = content.count(text)
        assert actual_count == count, u"Expected count of the text"\
               u" is %d, received = %d" % (count, actual_count)


@step(u"response code should be (\d+)")
def assert_response_code(step, status_code):
    """
    Generic step to check response code
    """
    status_code = int(status_code)

    response_code = world.response_code
    assert response_code == status_code, \
        "You've got %d status code, "\
            "expected one is %d" % (response_code, status_code)
