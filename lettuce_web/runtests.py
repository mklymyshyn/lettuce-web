import os
import lettuce


path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'features')

# below is snippet from lettuce original runner
run_controller = lettuce.RunController()
tag_checker = lettuce.core.TagChecker([])
run_controller.add(tag_checker)

runner = lettuce.Runner(path, scenarios=None,
                        verbosity=3,
                        enable_xunit=False,
                        xunit_filename=None,
                        run_controller=run_controller)

result = runner.run()
if not result or result.steps != result.steps_passed:
    raise SystemExit(1)
