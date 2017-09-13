from flask import request
from .exception import (
    MissingRepositoryId, InvalidRepositoryId, RepositoryNotFound,
    InvalidUserId, MissingUserId, RepositoryAccessDenied
)
from flask_security import current_user
from models import Repository


def safe_get_repository(repo_id_arg, user_id_arg=None):
    if repo_id_arg not in request.args:
        raise MissingRepositoryId(repo_id_arg)

    repo_id_str = request.args[repo_id_arg]
    try:
        repo_id = int(repo_id_str)
    except ValueError:
        raise InvalidRepositoryId('Failed to convert {} to {}'.format(repo_id_str, int))

    repo = Repository.query.get(repo_id)

    if repo is None:
        raise RepositoryNotFound(str(repo_id))

    if user_id_arg is None:
        user_id = current_user.id
    else:
        if user_id_arg not in request.args:
            raise MissingUserId(user_id_arg)

        user_id_str = request.args[user_id_arg]
        try:
            user_id = int(user_id_str)
        except ValueError:
            raise InvalidUserId('Failed to convert {} to {}'.format(user_id_str, int))

    if repo.user_id != user_id:
        raise RepositoryAccessDenied('User does not own the repository')

    return repo