from __future__ import annotations


class AppError(Exception):
    pass


class AuthorizationError(AppError):
    pass


class LogicError(AppError):
    pass


class PermissionDeniedError(AppError):
    pass
