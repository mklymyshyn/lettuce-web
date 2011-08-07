# -*- coding: utf-8 -*-

from lxml.html import HtmlElement

from lettuce import step, world, before
from nose.tools import assert_equal, assert_true, assert_raises


@before.each_step
def cleanup_attributes(step):
    """
    Shortcut to cleanup last page attributes
    from `world`
    """

    try:
        delattr(world, 'response_body')
        delattr(world, 'response_code')
        delattr(world, 'response')
    except AttributeError:
        pass

    with assert_raises(AttributeError):
        world.response_body
        world.response_code
        world.response


@step("Open url")
def test_open_url(step):
    step.given('I go to the "/" view')

    # check that response is 200
    assert_equal(world.response_code, 200)

    # check that we received requested page
    assert_true('Test Header' in world.response_body)

    # check that tree is parsed
    assert_true(isinstance(world.tree, HtmlElement))


@step("Open url without tree")
def test_open_url_without_tree(step):
    step.given('I go to the "/" view without tree')

    # make sure that text in place
    assert_true('Test Header' in world.response_body)

    assert_equal(world.tree, None)


@step("Open url by shortcut")
def test_open_url_by_shortcut(step):
    step.given('I go to the "test" view')

    # we should make sure that method `build_url`
    # was called and shourtcut processed respectively
    assert_equal(world.current_url, '/builded-view/')


@step("Open url with code 200")
def test_response_code_200(step):
    step.given('I go to the "/" view')

    assert_equal(world.response_code, 200)


@step("Open url with code 304")
def test_response_code_304(step):
    step.given('I go to the "/redirect" view')

    assert_equal(world.response_code, 304)


@step("Check that link exist")
def test_link_existing(step):
    step.given('I go to the "/" view')

    #step.given('')

