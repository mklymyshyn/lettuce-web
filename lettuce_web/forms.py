# -*- coding: utf-8 -*-

import itertools
import re

from lettuce import step, world


__all__ = ('assert_form_fields', 'fill_form_field', 'submit_form')


@step(u"There's form with following fields:")
def assert_form_fields(step):
    """
    Generic step to check particular fields existance on the page.

    Also this step may check array of values (eq checkboxes), like
        <input type="checkbox" name="theme_selections_1" />
        <input type="checkbox" name="theme_selections_2" />
        <input type="checkbox" name="theme_selections_3" />

    Usage example:
        There's form with following fields:
            | name |
            | email |
            | subject |
            | theme_selections_* |
    """

    # iterate through all `step.hashes` and make list of required fields
    fields = list(set([field for field in itertools.chain(
                                *[hs.values() for hs in step.hashes] +
                                 [hs.keys() for hs in step.hashes[0:1]])]))

    content, tree = world.response_body, world.tree
    vary_fields = [fields.pop(i) for i, fld in enumerate(fields)
                                                        if '*' in fld]

    fields_passed, vary_passed = False, False
    if len(vary_fields) == 0:
        vary_passed = True

    for form in tree.forms:
        input_names = form.inputs.keys()

        if not fields_passed and all([field in input_names
                                            for field in fields]):
            fields_passed = True

        # we don't need to check vary fields
        if len(vary_fields) == 0:
            continue

        vary_pass = []
        for field in vary_fields:
            try:
                prefix = field[0:field.index('*')]
            except ValueError:
                prefix = ''

            if any([input[0:len(prefix)] == prefix for input in input_names]):
                vary_pass.append(True)

        if fields_passed and len(vary_pass) == len(vary_fields):
            vary_passed = True
            break

    if fields_passed and vary_passed:
        return

    assert False, "There's no form on the page "\
                    "which have fields: %s" % ", ".join(fields + vary_fields)


@step(u'Fill the field "(.*)" with "(.*)"(.*)')
def fill_form_field(step, field, value, form_id):
    """
    Generic step to fill particular field on the page.

    It's possible to specify form id via "in form #<num>" sentence.

    NB: The count of forms starting from #1 !

    Usage example:
        Fill the field "name" with "Theodor"
        Fill the field "subject" with "Test subject" in form #1
    """

    try:
        form_num = int(re.findall(r'form #(\d+)', form_id)[0]) - 1
    except (ValueError, IndexError):
        form_num = None

    view = '<undefined>'
    content, tree = world.response_body, world.tree

    if hasattr(world, 'current_view'):
        view = world.current_view

    if len(tree.forms) == 0:
        assert False, "No forms appers on the page (%s view)" % view

    form = None
    for num, cur_form in enumerate(tree.forms):
        input_names = cur_form.inputs.keys()

        if not form_num is None and num == form_num and field in input_names:
            form = cur_form
            break

        if form_num is None and field in input_names:
            form = cur_form
            break

    assert form is not None, "There's no form with field '%s' (%s view)" % (
                        field, view)

    form.fields.update(((field, value),))


@step(u"Submit form #(\d+)(.*)")
def submit_form(step, form_num, follow):
    """
    Submit form with specific form number. If in body of
    feature exists text 'and follow' automatically
    follow by redirects and parse page with
    `url` method

    Examples:
        - Submit form #1
        - Submit form #2 and follow

    """
    kwargs = {}

    if follow and ' and follow' in follow:
        kwargs.update({
        'follow_redirects': True,
        })

    form_num = int(form_num)
    content, tree, env = world.response_body, world.tree, world.env

    if len(tree.forms) < form_num:
        assert False, "There's no form with #%d" % form_num

    form = tree.forms[form_num - 1]

    is_post = 'method' in form.attrib and \
                form.attrib['method'].lower() == 'post'

    if not form.action:
        # here should be same url as for world.response
        action = world.current_view
    else:
        action = form.action

    world.current_view = None
    world.response, world.response_code, world.response_body = env.url(
                                            url=action,
                                            post=is_post,
                                            tree=True,
                                            data=dict(form.fields.iteritems()),
                                            **kwargs)
