from __future__ import annotations

import uvicorn

from app.core.app import get_application
from app.core.config import settings

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
