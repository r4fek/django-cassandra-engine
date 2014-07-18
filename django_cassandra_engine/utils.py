import inspect
import cqlengine


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
