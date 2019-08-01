# __author__ = "xyt"

import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)

from conf import settings
from core import main


if __name__ == '__main__':
    main.run()