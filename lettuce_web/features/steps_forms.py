from lettuce import step, world
from nose.tools import assert_equal, assert_not_equal, assert_true


@step("Check that form on the page contain fields")
def test_form_contain_fields(step):
    step.given('I go to the "/" view')

    assert_true('<input type="text" name="name"' in \
                world.response_body)
    assert_true('<input type="text" name="email"' in \
                world.response_body)

    step.given("""
        There's form with following fields:
            | name |
            | email |

    """)


@step("Check that page contain array fields")
def test_form_not_contain_fields(step):
    step.given('I go to the "/" view')

    assert_equal(world.response_body.count(
                    '<input type="checkbox" name="theme_selections_'), 3)

    step.given("""
        There's form with following fields:
            | theme_selections_* |
    """)


@step("Fill form and check that it filled properly")
def test_fill_form_field(step):
    step.given('I go to the "/" view')

    data = {
        'name': 'name value',
        'email': 'test@example.com',
    }

    for name, val in data.iteritems():
        step.given('Fill the field "%s" with "%s"' % (name, val))

    # should be filled first form because
    # 'name' and 'email' fields should be in first form
    form = world.tree.forms[0]

    for name, val in data.iteritems():
        assert_equal(form.inputs[name].value, val)


@step("Fill field in particular form")
def test_fill_particular_form(step):
    step.given('I go to the "/" view')
    name, val = "name", "name val"
    step.given('Fill the field "%s" with "%s" in form #2' % (name, val))

    # should be filled first form because
    # 'name' and 'email' fields should be in first form
    form = world.tree.forms[1]

    assert_equal(form.inputs[name].value, val)
