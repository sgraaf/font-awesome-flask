from collections.abc import MutableMapping

from cookiecutter.utils import simple_filter


@simple_filter
def to_dict(value: MutableMapping):
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = to_dict(v)
    return dict(value)
