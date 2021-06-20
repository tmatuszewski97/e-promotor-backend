import environ

from .base import *
from pathlib import Path

if env('PROJECT_MODE') == 'production':
    from .prod import *
else:
    from .dev import *
