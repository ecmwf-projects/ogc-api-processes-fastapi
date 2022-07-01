# Copyright 2022, European Union.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

from __future__ import annotations

import enum
from typing import Any, Union, cast

import pydantic


class Metadata(pydantic.BaseModel):
    title: str | None = None
    role: str | None = None
    href: str | None = None


class AdditionalParameter(pydantic.BaseModel):
    name: str
    value: list[Union[str, float, int, list[Any], dict[str, Any]]]


class JobControlOptions(enum.Enum):
    sync_execute: str = "sync-execute"
    async_execute: str = "async-execute"
    dismiss: str = "dismiss"


class TransmissionMode(enum.Enum):
    value: str = "value"
    reference: str = "reference"


class Link(pydantic.BaseModel):
    href: str
    rel: str | None = pydantic.Field(None, example="service")
    type: str | None = pydantic.Field(None, example="application/json")
    hreflang: str | None = pydantic.Field(None, example="en")
    title: str | None = None


class AdditionalParameters(Metadata):
    parameters: list[AdditionalParameter] | None = None


class DescriptionType(pydantic.BaseModel):
    title: str | None = None
    description: str | None = None
    keywords: list[str] | None = None
    metadata: list[Metadata] | None = None
    additionalParameters: AdditionalParameters | None = None


class ProcessSummary(DescriptionType):
    id: str
    version: str
    jobControlOptions: list[JobControlOptions] | None = None
    outputTransmission: list[TransmissionMode] | None = None
    links: list[Link] | None = None


class ProcessesList(pydantic.BaseModel):
    processes: list[ProcessSummary]
    links: list[Link]


class MaxOccur(enum.Enum):
    unbounded = "unbounded"


class Type(enum.Enum):
    array = "array"
    boolean = "boolean"
    integer = "integer"
    number = "number"
    object = "object"
    string = "string"


class Reference(pydantic.BaseModel):
    _ref: str = pydantic.Field(..., alias="$ref")


class PositiveInt(pydantic.ConstrainedInt):
    ge = 0


class SchemaItem(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

    title: str | None = None
    multipleOf: pydantic.PositiveFloat | None = None
    maximum: float | None = None
    exclusiveMaximum: bool | None = False
    minimum: float | None = None
    exclusiveMinimum: bool | None = False
    maxLength: PositiveInt | None = None
    minLength: PositiveInt | None = cast(PositiveInt, 0)
    pattern: str | None = None
    maxItems: PositiveInt | None = None
    minItems: PositiveInt | None = cast(PositiveInt, 0)
    uniqueItems: bool | None = False
    maxProperties: PositiveInt | None = None
    minProperties: PositiveInt | None = cast(PositiveInt, 0)
    required: list[str] | None = pydantic.Field(None, min_items=1)
    enum: list[Any] | None = pydantic.Field(None, min_items=1)
    type: Type | None = None
    description: str | None = None
    format: str | None = None
    default: Any | None = None
    nullable: bool | None = False
    readOnly: bool | None = False
    writeOnly: bool | None = False
    example: Any | None = None
    deprecated: bool | None = False
    contentMediaType: str | None = None
    contentEncoding: str | None = None
    contentSchema: str | None = None


class Schema(pydantic.BaseModel):
    __root__: Union[Reference, SchemaItem]


class InputDescription(DescriptionType):
    minOccurs: int | None = 1
    maxOccurs: Union[int, MaxOccur] | None = None
    schema_: Schema = pydantic.Field(..., alias="schema")


class OutputDescription(DescriptionType):
    schema_: Schema = pydantic.Field(..., alias="schema")


class Process(ProcessSummary):
    inputs: InputDescription | None
    outputs: OutputDescription | None
