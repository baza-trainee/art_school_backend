import inspect
from typing import Type

from pydantic import BaseModel


# Decorator for PATCH methods, to create a form in Swagger.
def as_form_patch(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, field_type in cls.__annotations__.items():
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=None,
                annotation=field_type,
            )
        )

    async def as_form_patch_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_patch_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_patch_func.__signature__ = sig
    setattr(cls, "as_form_patch", as_form_patch_func)
    return cls
