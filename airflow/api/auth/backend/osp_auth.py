import airflow

from functools import wraps
from flask import Response, request
from airflow import models, settings


current_user = airflow.login.current_user
dagbag = models.DagBag(settings.DAGS_FOLDER)


def osp_allow_superuser_only(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if current_user.is_superuser():
            return function(*args, **kwargs)
        return Response("Forbidden", 403)

    return decorated


def osp_expose_only_owned_entities(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if current_user.is_superuser():
            return function(*args, **kwargs)

        dag_id = request.args.get('dag_id')
        dag = dagbag.get_dag(dag_id)

        if dag and dag.owner in current_user.osp_groups:
            return function(*args, **kwargs)

        return Response("Forbidden", 403)

    return decorated
