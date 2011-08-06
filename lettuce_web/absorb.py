from lettuce import after, before, world


def get_env():
    """
    Shortcut to get environment from `world` or initialize it
    """

    obj = getattr(world, 'env', None) or world.webenv_class(world)

    if not obj:
        raise Warning(u"Lettuce-Web environment not initialized")
        return None

    world.env = obj
    return obj


@world.absorb
def set_up():
    """
    Method which should be called in
    @before.each_scenario
    """

    obj = get_env()

    if obj:
        obj.set_up()


@world.absorb
def tear_down():
    """
    Method which should be called in
    @after.each_scenario
    """

    obj = get_env()

    if obj:
        obj.tear_down()


@before.each_scenario
def setup_scenario(scenario):
    """
    Setup test environment for each scenario
    """
    world.set_up()


@after.each_scenario
def teardown_scenario(scenario):
    """
    Teardown test environment for
    each scenario
    """
    world.tear_down()


@before.all
def bootstrap_environ():
    """
    Bootstrap environment
    """
    obj = get_env()
    obj.bootstrap()
    world.env = obj


@after.all
def destroy_environ():
    """
    Destroy test environment
    """
    obj = get_env()
    obj.destroy()
