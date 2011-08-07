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
