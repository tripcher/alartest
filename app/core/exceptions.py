from __future__ import annotations


class AppError(Exception):
    pass


class AuthorizationError(AppError):
    pass
