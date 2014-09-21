import inspect
import cqlengine
import django


def get_installed_apps():
    if django.VERSION >= (1, 7):
        from django.apps import apps
        return apps.get_apps()
    else:
        from django.db import models
        return models.get_apps()


def get_cql_models(app):
    """
    :param app: django models module
    :return: list of all cqlengine.Model within app
    """

    models = []
    for name, obj in inspect.getmembers(app):
        if inspect.isclass(obj) and issubclass(obj, cqlengine.Model) \
                and not obj.__abstract__:
            models.append(obj)

    return models
