import airflow

from functools import wraps
from flask import Response, request
from airflow import models, settings

from flask_admin.contrib.sqla.filters import FilterInList

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

        # Here I assume that url encoded filter for dag_id is under flt1
        dag_id = request.args.get('dag_id') or request.args.get('flt1_dag_id_equals')
        dag = dagbag.get_dag(dag_id)

        if dag and dag.owner in current_user.osp_groups:
            return function(*args, **kwargs)

        return Response("Forbidden", 403)

    return decorated


class DagOwnerInList(FilterInList):
    def __init__(self):
        column = 'owner'
        name = 'osp_dag_owner'
        options = None
        data_type='select2-tags'
        super(FilterInList, self).__init__(column, name, options, data_type)

    def clean(self, value):
        return current_user.osp_groups
