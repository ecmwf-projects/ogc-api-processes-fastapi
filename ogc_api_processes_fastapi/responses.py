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

import enum
from datetime import datetime
from typing import Any, Dict, ForwardRef, List, Optional, Tuple, Type, Union, cast

import pydantic


class ExtraForbidConfig:
    extra = pydantic.Extra.forbid


def generate_schema(add_params: Dict[str, Dict[str, Tuple[Type, Any]]] = None):

    if not add_params:
        add_params = {}

    Metadata = pydantic.create_model(
        "Metadata",
        title=(Optional[str], None),
        role=(Optional[str], None),
        href=(Optional[str], None),
    )
    AdditionalParameter = pydantic.create_model(
        "AdditionalParameter",
        name=(str, ...),
        value=(List[Union[str, float, int, List[Any], Dict[str, Any]]], ...),
    )
    Link = pydantic.create_model(
        "Link",
        href=(str, ...),
        rel=(Optional[str], pydantic.Field(None, example="service")),
        type=(Optional[str], pydantic.Field(None, example="application/json")),
        hreflang=(Optional[str], pydantic.Field(None, example="en")),
        title=(Optional[str], None),
    )

    class JobControlOptions(enum.Enum):
        sync_execute: str = "sync-execute"
        async_execute: str = "async-execute"
        dismiss: str = "dismiss"

    class TransmissionMode(enum.Enum):
        value: str = "value"
        reference: str = "reference"

    ConfClass = pydantic.create_model(
        "ConfClass",
        conformsTo=(
            List[str],
            pydantic.Field(
                example="http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core"
            ),
        ),
    )

    class AdditionalParameters(Metadata):
        parameters: Optional[List[AdditionalParameter]] = None

    DescriptionType = pydantic.create_model(
        "DescriptionType",
        title=(Optional[str], None),
        description=(Optional[str], None),
        keywords=(Optional[List[str]], None),
        metadata=(Optional[List[Metadata]], None),
        additionalParameters=(Optional[AdditionalParameters], None),
    )

    class ProcessSummary(DescriptionType):
        id: str
        version: str
        jobControlOptions: Optional[List[JobControlOptions]] = None
        outputTransmission: Optional[List[TransmissionMode]] = None
        links: Optional[List[Link]] = None

    ProcessesList = pydantic.create_model(
        "ProcessesList", processes=(List[ProcessSummary], ...), links=(List[Link], ...)
    )

    class MaxOccur(enum.Enum):
        unbounded = "unbounded"

    class ObjectType(enum.Enum):
        array = "array"
        boolean = "boolean"
        integer = "integer"
        number = "number"
        object = "object"
        string = "string"

    Reference = pydantic.create_model(
        "Reference",
        ref=(str, pydantic.Field(..., alias="$ref")),
        __config__=ExtraForbidConfig,
    )

    class PositiveInt(pydantic.ConstrainedInt):
        ge = 0

    SchemaItem = ForwardRef("SchemaItem")

    SchemaItem = pydantic.create_model(
        "SchemaItem",
        title=(Optional[str], None),
        multipleO=(Optional[pydantic.PositiveFloat], None),
        maximum=(Optional[float], None),
        exclusiveMaximum=(Optional[bool], False),
        minimum=(Optional[float], None),
        exclusiveMinimum=(Optional[bool], False),
        maxLength=(Optional[PositiveInt], None),
        minLength=(Optional[PositiveInt], cast(PositiveInt, 0)),
        pattern=(Optional[str], None),
        maxItems=(Optional[PositiveInt], None),
        minItems=(Optional[PositiveInt], cast(PositiveInt, 0)),
        uniqueItems=(Optional[bool], False),
        maxProperties=(Optional[PositiveInt], None),
        minProperties=(Optional[PositiveInt], cast(PositiveInt, 0)),
        required=(Optional[List[str]], pydantic.Field(None, min_items=1)),
        enum=(Optional[List[Any]], pydantic.Field(None, min_items=1)),
        type=(Optional[ObjectType], None),
        description=(Optional[str], None),
        format=(Optional[str], None),
        default=(Optional[Any], None),
        nullable=(Optional[bool], False),
        readOnly=(Optional[bool], False),
        writeOnly=(Optional[bool], False),
        example=(Optional[Any], None),
        deprecated=(Optional[bool], False),
        contentMediaType=(Optional[str], None),
        contentEncoding=(Optional[str], None),
        contentSchema=(Optional[str], None),
        items=(Optional[Union[Reference, SchemaItem]], None),
        properties=(Optional[Dict[str, Union[Reference, SchemaItem]]], None),
        __config__=ExtraForbidConfig,
    )

    SchemaItem.update_forward_refs()

    class InputDescription(DescriptionType):
        class Config:
            allow_population_by_field_name = True

        minOccurs: Optional[int] = 1
        maxOccurs: Optional[Union[int, MaxOccur]] = None
        schema_: Union[Reference, SchemaItem] = pydantic.Field(..., alias="schema")

    class OutputDescription(DescriptionType):
        class Config:
            allow_population_by_field_name = True

        schema_: Union[Reference, SchemaItem] = pydantic.Field(..., alias="schema")

    class BinaryInputValue(pydantic.BaseModel):
        __root__: str

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

    class InputValueNoObject(pydantic.BaseModel):
        __root__: Union[str, float, int, bool, List[Any], BinaryInputValue, Bbox]

    class Format(pydantic.BaseModel):
        mediaType: Optional[str] = None
        encoding: Optional[str] = None
        schema_: Optional[Union[str, Dict[str, Any]]] = pydantic.Field(
            None, alias="schema"
        )

    class InputValue(pydantic.BaseModel):
        __root__: Union[InputValueNoObject, Dict[str, Any]]

    class QualifiedInputValue(Format):
        value: InputValue

    class InlineOrRefData(pydantic.BaseModel):
        __root__: Union[InputValueNoObject, QualifiedInputValue, Link]

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
        inputs: Optional[
            Dict[str, Union[InlineOrRefData, List[InlineOrRefData]]]
        ] = None
        outputs: Optional[Dict[str, Output]] = None
        response: Optional[Response] = Response.raw
        subscriber: Optional[Subscriber] = None

    class ProcessDescription(ProcessSummary):
        inputs: Optional[Dict[str, InputDescription]] = None
        outputs: Optional[Dict[str, OutputDescription]] = None

    class ConInt(pydantic.ConstrainedInt):
        ge = 0
        le = 100

    class StatusCode(enum.Enum):
        accepted = "accepted"
        running = "running"
        successful = "successful"
        failed = "failed"
        dismissed = "dismissed"

    class JobType(enum.Enum):
        process = "process"

    class StatusInfo(pydantic.BaseModel):
        processID: Optional[str] = None
        type: JobType
        jobID: str
        status: StatusCode
        message: Optional[str] = None
        created: Optional[datetime] = None
        started: Optional[datetime] = None
        finished: Optional[datetime] = None
        updated: Optional[datetime] = None
        progress: Optional[ConInt] = None
        links: Optional[List[Link]] = None

    class JobList(pydantic.BaseModel):
        jobs: List[StatusInfo]
        links: List[Link]

    class Results(pydantic.BaseModel):
        __root__: Optional[Dict[str, InlineOrRefData]] = None

    class Exception(pydantic.BaseModel):
        class Config:
            extra = pydantic.Extra.allow

        type: str
        title: Optional[str] = None
        status: Optional[int] = None
        detail: Optional[str] = None
        instance: Optional[str] = None

    class LandingPage(pydantic.BaseModel):
        title: Optional[str] = pydantic.Field(
            default=None, example="Example processing server"
        )
        description: Optional[str] = pydantic.Field(
            default=None,
            example="Example server implementing the OGC API - Processes 1.0 Standard",
        )
        links: List[Link]

    return {
        "GetLandingPage": LandingPage,
        "GetConformance": ConfClass,
        "GetProcesses": ProcessesList,
        "GetProcess": ProcessDescription,
        "PostProcessExecute": StatusInfo,
        "GetJobs": JobList,
        "GetJob": StatusInfo,
        "GetJobResults": Results,
    }
