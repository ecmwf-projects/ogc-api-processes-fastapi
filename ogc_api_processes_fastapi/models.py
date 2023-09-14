"""OGC API Processes responses and requests models."""

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

import datetime
import enum
from typing import Any, Dict, ForwardRef, List, Optional, Union, cast

import pydantic
import typing_extensions


class Metadata(pydantic.BaseModel):
    title: Optional[str] = None
    role: Optional[str] = None
    href: Optional[str] = None


class AdditionalParameter(pydantic.BaseModel):
    name: str
    value: List[Union[str, float, int, List[Any], Dict[str, Any]]]


class JobControlOptions(enum.Enum):
    sync_execute: str = "sync-execute"
    async_execute: str = "async-execute"
    dismiss: str = "dismiss"


class TransmissionMode(enum.Enum):
    value: str = "value"  # type:ignore
    reference: str = "reference"


class PaginationQueryParameters(pydantic.BaseModel):
    next: Optional[Dict[str, str]] = None
    prev: Optional[Dict[str, str]] = None


class Link(pydantic.BaseModel):
    href: str
    rel: Optional[str] = pydantic.Field(None, json_schema_extra={"example": "service"})
    type: Optional[str] = pydantic.Field(
        None, json_schema_extra={"example": "application/json"}
    )
    hreflang: Optional[str] = pydantic.Field(None, json_schema_extra={"example": "en"})
    title: Optional[str] = None


class LandingPage(pydantic.BaseModel):
    title: Optional[str] = pydantic.Field(
        default=None, json_schema_extra={"example": "Example processing server"}
    )
    description: Optional[str] = pydantic.Field(
        default=None,
        json_schema_extra={
            "example": "Example server implementing the OGC API - Processes 1.0 Standard"
        },
    )
    links: List[Link]


class ConfClass(pydantic.BaseModel):
    conformsTo: List[str] = pydantic.Field(
        json_schema_extra={
            "example": "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core"
        }
    )


class AdditionalParameters(Metadata):
    parameters: Optional[List[AdditionalParameter]] = None


class DescriptionType(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    metadata: Optional[List[Metadata]] = None
    additionalParameters: Optional[AdditionalParameters] = None


class ProcessSummary(DescriptionType):
    id: str
    version: str
    jobControlOptions: Optional[List[JobControlOptions]] = None
    outputTransmission: Optional[List[TransmissionMode]] = None
    links: Optional[List[Link]] = None


class ProcessList(pydantic.BaseModel):
    processes: List[ProcessSummary]
    links: List[Link]
    _pagination_query_params: Optional[PaginationQueryParameters] = None


class MaxOccur(enum.Enum):
    unbounded = "unbounded"


class ObjectType(enum.Enum):
    array = "array"
    boolean = "boolean"
    integer = "integer"
    number = "number"
    object = "object"
    string = "string"


class Reference(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")
    ref: str


PositiveInt = typing_extensions.Annotated[int, pydantic.Field(ge=0)]


SchemaItem = ForwardRef("SchemaItem")


class SchemaItem(pydantic.BaseModel):  # type: ignore
    model_config = pydantic.ConfigDict(extra="forbid")

    title: Optional[str] = None
    multipleOf: Optional[pydantic.PositiveFloat] = None
    maximum: Optional[float] = None
    exclusiveMaximum: Optional[bool] = False
    minimum: Optional[float] = None
    exclusiveMinimum: Optional[bool] = False
    maxLength: Optional[PositiveInt] = None
    minLength: Optional[PositiveInt] = cast(PositiveInt, 0)
    pattern: Optional[str] = None
    maxItems: Optional[PositiveInt] = None
    minItems: Optional[PositiveInt] = cast(PositiveInt, 0)
    uniqueItems: Optional[bool] = False
    maxProperties: Optional[PositiveInt] = None
    minProperties: Optional[PositiveInt] = cast(PositiveInt, 0)
    required: Optional[List[str]] = pydantic.Field(None, min_length=1)
    enum: Optional[List[Any]] = pydantic.Field(None, min_length=1)
    type: Optional[ObjectType] = None
    description: Optional[str] = None
    format: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = False
    readOnly: Optional[bool] = False
    writeOnly: Optional[bool] = False
    example: Optional[Any] = None
    deprecated: Optional[bool] = False
    contentMediaType: Optional[str] = None
    contentEncoding: Optional[str] = None
    contentSchema: Optional[str] = None
    items: Optional[Union[Reference, SchemaItem]] = None  # type: ignore
    properties: Optional[Dict[str, Union[Reference, SchemaItem]]] = None  # type: ignore


SchemaItem.model_rebuild()  # type: ignore


class InputDescription(DescriptionType):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    minOccurs: Optional[int] = 1
    maxOccurs: Optional[Union[int, MaxOccur]] = None
    schema_: Union[Reference, SchemaItem] = pydantic.Field(..., alias="schema")  # type: ignore


class OutputDescription(DescriptionType):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    schema_: Union[Reference, SchemaItem] = pydantic.Field(..., alias="schema")  # type: ignore


BinaryInputValue = pydantic.RootModel[str]


class Crs(enum.Enum):
    http___www_opengis_net_def_crs_OGC_1_3_CRS84 = (
        "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    )
    http___www_opengis_net_def_crs_OGC_0_CRS84h = (
        "http://www.opengis.net/def/crs/OGC/0/CRS84h"
    )


class Bbox(pydantic.BaseModel):
    bbox: List[float]
    crs: Optional[Crs] = Crs.http___www_opengis_net_def_crs_OGC_1_3_CRS84


InputValueNoObject = pydantic.RootModel[
    Union[str, float, int, bool, List[Any], BinaryInputValue, Bbox]
]


class Format(pydantic.BaseModel):
    mediaType: Optional[str] = None
    encoding: Optional[str] = None
    schema_: Optional[Union[str, Dict[str, Any]]] = pydantic.Field(None, alias="schema")


InputValue = pydantic.RootModel[Union[Dict[str, Any], InputValueNoObject]]


class QualifiedInputValue(Format):
    value: InputValue


InlineOrRefData = pydantic.RootModel[
    Union[InputValueNoObject, QualifiedInputValue, Link]
]


class Output(pydantic.BaseModel):
    format: Optional[Format] = None
    transmissionMode: Optional[TransmissionMode] = None


class Response(enum.Enum):
    raw = "raw"
    document = "document"


class Subscriber(pydantic.BaseModel):
    successUri: Optional[pydantic.AnyUrl] = None
    inProgressUri: Optional[pydantic.AnyUrl] = None
    failedUri: Optional[pydantic.AnyUrl] = None


class Execute(pydantic.BaseModel):
    inputs: Optional[Dict[str, Union[InlineOrRefData, List[InlineOrRefData]]]] = None
    outputs: Optional[Dict[str, Output]] = None
    response: Optional[Response] = Response.raw
    subscriber: Optional[Subscriber] = None


class ProcessDescription(ProcessSummary):
    inputs: Optional[Dict[str, InputDescription]] = None
    outputs: Optional[Dict[str, OutputDescription]] = None


ConInt = typing_extensions.Annotated[int, pydantic.Field(ge=0, le=100)]


class StatusCode(str, enum.Enum):
    accepted: str = "accepted"
    running: str = "running"
    successful: str = "successful"
    failed: str = "failed"
    dismissed: str = "dismissed"


class JobType(enum.Enum):
    process = "process"


class StatusInfo(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="allow")

    processID: Optional[str] = None
    type: JobType
    jobID: str
    status: StatusCode
    message: Optional[str] = None
    created: Optional[datetime.datetime] = None
    started: Optional[datetime.datetime] = None
    finished: Optional[datetime.datetime] = None
    updated: Optional[datetime.datetime] = None
    progress: Optional[ConInt] = None
    links: Optional[List[Link]] = None


class JobList(pydantic.BaseModel):
    jobs: List[StatusInfo]
    links: Optional[List[Link]] = None
    _pagination_query_params: Optional[PaginationQueryParameters] = None


class Results(pydantic.RootModel[Dict[str, InlineOrRefData]]):
    root: Optional[Dict[str, InlineOrRefData]] = None


class Exception(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="allow")

    type: str
    title: Optional[str] = None
    status: Optional[int] = None
    detail: Optional[str] = None
    instance: Optional[str] = None
