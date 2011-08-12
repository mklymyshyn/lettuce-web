Lettuce Web
====================

*Behavior Driven Development (BDD) abstract web driver for
[lettuce](http://lettuce.it)*

### The Problem

Lettuce is great tool to using BDD approach on the project. But the problem
is that sometimes we not use django to create websites. Sometimes we aren't use
even python. In this case we need to create some environment to concentrate
our efforts on testing rather than fall into routine things like opening url or parsing forms.

### The Solution

*Lettuce Web* will take care of routine steps. Here is form parser, typical
things like `assert_url`, `assert_form_fields` or `assert_contains`.
The only thing on you is provide *driver* for your framework or
application.



Internals
--------------------

To create instance of your environment you should add it to `world`.
Example:

        from lettuce import world
        from mylib import ImplementedEnvironment


        world.webenv_class = ImplementedEnvironment



The work of setup/teardown of the environment have strict order:

  1. In `@before.all` `env_instance.bootstrap()` method will be called, then
  1. In `@before.each_scenario` will be called `env_instance.set_up()`
  1. And in `@after.each_scenario` will be called `env_instance.tear_down()`
  1. At last, in `@after.all` will be called `env_instance.destroy()`


Step Matchers
--------------------

The following lettuce step matchers are included in this package and can be used with Given/When/Then/And as desired.

  1. `I go to the "home" view` - go to "home" view. You may specify both
  url or specific or named url as argument but you also should care about
  resolving named urls in `build_url` method of your driver.
  1. `I go to the "/" view without tree` - go to the view but without building 
  LXML tree
  1. Check that form with provided fields exist on the page:

        There's form with following fields:
            | name |
            | email |
            | theme_selections_* |

  1. Fill specified field with provided value:
  `Fill the field "email" with "me@example.com"`
  1. Fill specified field with provided value in specific form:
  `Fill the field "email" with "me@example.com" in form #1`
  1. Submit form with `Submit form #1`. The index of forms order
  starting from **1**.
