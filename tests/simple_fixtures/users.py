from __future__ import annotations

import pytest

from app.users.dto import User
from app.users.selectors import find_user_by_username
from app.users.tables import users

