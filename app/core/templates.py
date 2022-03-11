from __future__ import annotations

import os

from starlette.templating import Jinja2Templates

from app.core.config import settings

templates = Jinja2Templates(directory=os.path.join(settings.BASE_DIR, "templates"))
