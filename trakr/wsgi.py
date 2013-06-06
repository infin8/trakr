import os
os.chdir(os.path.dirname(__file__))

import controller

application = controller.bottle.default_app()
