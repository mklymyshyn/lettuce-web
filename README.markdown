Lettuce Web
====================

*Behavior Driven Development (BDD) abstract web driver for
[lettuce](http://lettuce.it)*


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
