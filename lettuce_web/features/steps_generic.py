# -*- coding: utf-8 -*-

from lxml.html import HtmlElement

from lettuce import step, world
from nose.tools import assert_equal, assert_false, \
                       assert_is_not_none, assert_true


@step("Open url")
def test_open_url(step):
    step.given('I go to the "/" view')

    # check that page is loaded
    assert_is_not_none(getattr(world, 'response_body'))
    assert_is_not_none(getattr(world, 'response_code'))
    assert_is_not_none(getattr(world, 'response'))
    assert_is_not_none(getattr(world, 'tree'))

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
def test_link_exist(step):
    step.given('I go to the "/" view')

    # check firstly that link exist on the page
    assert_true('href="/builded-view/"' in world.response_body)

    # then check that step work as expected
    step.given('Should be link to "test" view')

    # check that url exist on the page too
    step.given('Should be link to "/builded-view/" view')

    # TODO: we should take care about more complex urls like
    #   - /testurl/?test
    #   - /testurl/#test


@step("Check that link doesn't exist")
def test_link_not_exist(step):
    step.given('I go to the "/" view')

    # check that link not exist on the page
    assert_false('href="/"' in world.response_body)

    # then check that step work as expected
    step.given('Shouldn\'t be link to "/" view')
    step.given('Should not be link to "/" view')


@step("Check that body contains string")
def test_body_contains_string(step):
    step.given('I go to the "/" view')

    assert_true('Important test' in world.response_body)

    step.given('Page body contain "Important test"')


@step("Check that body doesn't contain string")
def test_body_not_contain_string(step):
    step.given('I go to the "/" view')

    assert_false('No test' in world.response_body)

    step.given('Page body not contain "No test"')


@step("Check that body contain string exactly 2 times")
def test_body_contain_string_2times(step):
    step.given('I go to the "/" view')

    assert_equal(world.response_body.count('Important test'), 2)

    step.given('Page body contain "Important test", exactly 2 times')
