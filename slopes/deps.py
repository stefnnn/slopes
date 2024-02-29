from fastapi import Depends, Request

from slopes.controllers.app import GlobalState
from slopes.models import User
from slopes.plugins.auth.dependencies import AuthDependencies


def get_global_state(user: User = Depends(AuthDependencies.peek_user(User))):
    return GlobalState(logged_in_user=user)