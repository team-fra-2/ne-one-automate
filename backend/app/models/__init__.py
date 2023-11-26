from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

"""
Generated: 2022-10-11
"""


class Thing(BaseModel):
    id: str = Field(default=None, alias="@id")

    class Config:
        populate_by_name = True
        alias_generator = to_camel
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ")}
