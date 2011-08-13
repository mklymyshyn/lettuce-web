import os
import lettuce

paths = [
'features',
'drivers/flask/features',
]

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

#path = os.path.join(BASE_PATH, 'features')

# below is snippet from lettuce original runner
run_controller = lettuce.RunController()
tag_checker = lettuce.core.TagChecker([])
run_controller.add(tag_checker)


for path in paths:
    path = os.path.join(BASE_PATH, path)
    runner = lettuce.Runner(path, scenarios=None,
                            verbosity=3,
                            enable_xunit=False,
                            xunit_filename=None,
                            run_controller=run_controller)

    result = runner.run()
