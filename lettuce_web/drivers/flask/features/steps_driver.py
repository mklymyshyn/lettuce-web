# -*- coding: utf-8 -*-

from lettuce import step, world
from nose.tools import assert_equal


@step(u'Build URL to several Flask views')
def build_url_to_the_view(step):

    assert_equal(world.env.build_url("home"), "/")

    assert_equal(world.env.build_url("subpage"), "/subpage/")

    assert_equal(world.env.build_url("/directurl/"), '/directurl/')


@step(u'Download URL from Flask App')
def download_url_from_flask_app(step):

    step.given(u'I go to the "home" view')
    assert_equal(world.response_body, 'home page')

    step.given(u'I go to the "subpage" view')
    assert_equal(world.response_body, 'sub page')

    step.given(u'I go to the "/nonexisting/" view')

    assert_equal(world.response_code, 404)


@step(u'Make POST request to the Flask App')
def make_post_request_to_the_flask_app(step):
    data = {
        'name': 'name val',
        'email': 'test@test.com',
    }

    response, response_code, response_body = world.env.url(url="post",
                                                    post=True, data=data)

    assert_equal(response_code, 200)
    assert_equal(response_body, "\n".join(["%s=%s" % (name, val) \
                                    for name, val in data.iteritems()]))
