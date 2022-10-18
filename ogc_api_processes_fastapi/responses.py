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


def generate_schema(add_params: Dict[str, Dict[str, Tuple[Type, Any]]] = None):

    if not add_params:
        add_params = {}

    schema = {}

    class ExtraForbidConfig(pydantic.BaseConfig):
        extra = pydantic.Extra.forbid
        use_enum_values = True

    class ExtraAllowConfig(pydantic.BaseConfig):
        extra = pydantic.Extra.allow
        use_enum_values = True

    class AllowPopulationFieldByName(ExtraAllowConfig):
        allow_population_by_field_name = True

    class JobControlOptions(enum.Enum):
        sync_execute: str = "sync-execute"
        async_execute: str = "async-execute"
        dismiss: str = "dismiss"

    class TransmissionMode(enum.Enum):
        value: str = "value"
        reference: str = "reference"

    class MaxOccur(enum.Enum):
        unbounded = "unbounded"

    class ObjectType(enum.Enum):
        array = "array"
        boolean = "boolean"
        integer = "integer"
        number = "number"
        object = "object"
        string = "string"

    class PositiveInt(pydantic.ConstrainedInt):
        ge = 0

    class BinaryInputValue(pydantic.BaseModel):
        __root__: str

    class Crs(enum.Enum):
        http___www_opengis_net_def_crs_OGC_1_3_CRS84 = (
            "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        )
        http___www_opengis_net_def_crs_OGC_0_CRS84h = (
            "http://www.opengis.net/def/crs/OGC/0/CRS84h"
        )

    class Response(enum.Enum):
        raw = "raw"
        document = "document"

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

    schema["Metadata"] = pydantic.create_model(
        "Metadata",
        __config__=ExtraAllowConfig,
        title=(Optional[str], None),
        role=(Optional[str], None),
        href=(Optional[str], None),
        **add_params.get("Metadata", {}),
    )
    schema["AdditionalParameter"] = pydantic.create_model(
        "AdditionalParameter",
        __config__=ExtraAllowConfig,
        name=(str, ...),
        value=(List[Union[str, float, int, List[Any], Dict[str, Any]]], ...),
        **add_params.get("AdditionalParameter", {}),
    )
    schema["Link"] = pydantic.create_model(
        "Link",
        __config__=ExtraAllowConfig,
        href=(str, ...),
        rel=(Optional[str], pydantic.Field(None, example="service")),
        type=(Optional[str], pydantic.Field(None, example="application/json")),
        hreflang=(Optional[str], pydantic.Field(None, example="en")),
        title=(Optional[str], None),
        **add_params.get("Link", {}),
    )
    schema["ConfClass"] = pydantic.create_model(
        "ConfClass",
        __config__=ExtraAllowConfig,
        conformsTo=(
            List[str],
            pydantic.Field(
                example="http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core"
            ),
        ),
        **add_params.get("ConfClass", {}),
    )
    schema["AdditionalParameters"] = pydantic.create_model(
        "AdditionalParameters",
        __base__=schema["Metadata"],
        parameters=(Optional[List[schema["AdditionalParameter"]]], None),  # noqa
        **add_params.get("AdditionalParameters", {}),
    )
    schema["DescriptionType"] = pydantic.create_model(
        "DescriptionType",
        __config__=AllowPopulationFieldByName,
        title=(Optional[str], None),
        description=(Optional[str], None),
        keywords=(Optional[List[str]], None),
        metadata=(Optional[List[schema["Metadata"]]], None),  # noqa
        additionalParameters=(Optional[schema["AdditionalParameters"]], None),  # noqa
        **add_params.get("DescriptionType", {}),
    )
    schema["ProcessSummary"] = pydantic.create_model(
        "ProcessSummary",
        __base__=schema["DescriptionType"],
        id=(str, ...),
        version=(str, ...),
        jobControlOptions=(Optional[List[JobControlOptions]], None),
        outputTransmission=(Optional[List[TransmissionMode]], None),
        links=(Optional[List[schema["Link"]]], None),  # noqa
        **add_params.get("ProcessSummary", {}),
    )
    schema["ProcessesList"] = pydantic.create_model(
        "ProcessesList",
        __config__=ExtraAllowConfig,
        processes=(List[schema["ProcessSummary"]], ...),  # noqa
        links=(List[schema["Link"]], ...),  # noqa
        **add_params.get("ProcessesList", {}),
    )
    schema["Reference"] = pydantic.create_model(
        "Reference",
        __config__=ExtraForbidConfig,
        ref=(str, pydantic.Field(..., alias="$ref")),
    )
    schema["SchemaItem"] = ForwardRef("SchemaItem")
    schema["SchemaItem"] = pydantic.create_model(
        "SchemaItem",
        __config__=ExtraForbidConfig,
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
        items=(
            Optional[Union[schema["Reference"], schema["SchemaItem"]]],  # noqa
            None,
        ),  # noqa
        properties=(
            Optional[
                Dict[str, Union[schema["Reference"], schema["SchemaItem"]]]  # noqa
            ],  # noqa
            None,
        ),
    )
    schema["SchemaItem"].update_forward_refs()

    schema["InputDescription"] = pydantic.create_model(
        "InputDescription",
        __base__=schema["DescriptionType"],
        minOccurs=(Optional[int], 1),
        maxOccurs=(Optional[Union[int, MaxOccur]], None),
        schema_=(
            Union[schema["Reference"], schema["SchemaItem"]],  # noqa
            pydantic.Field(..., alias="schema"),
        ),
        **add_params.get("InputDescription", {}),
    )
    schema["OutputDescription"] = pydantic.create_model(
        "OutputDescription",
        __base__=schema["DescriptionType"],
        schema_=(
            Union[schema["Reference"], schema["SchemaItem"]],  # noqa
            pydantic.Field(..., alias="schema"),
        ),
        **add_params.get("OutputDescription", {}),
    )
    schema["Bbox"] = pydantic.create_model(
        "Bbox",
        __config__=ExtraAllowConfig,
        bbox=(List[float], ...),
        crs=(Optional[Crs], Crs.http___www_opengis_net_def_crs_OGC_1_3_CRS84),
        **add_params.get("Bbox", {}),
    )

    class InputValueNoObject(pydantic.BaseModel):
        __root__: Union[
            str, float, int, bool, List[Any], BinaryInputValue, schema["Bbox"]  # noqa
        ]

    schema["InputValueNoObject"] = InputValueNoObject
    schema["Format"] = pydantic.create_model(
        "Format",
        __config__=ExtraAllowConfig,
        mediaType=(Optional[str], None),
        encoding=(Optional[str], None),
        schema_=(
            Optional[Union[str, Dict[str, Any]]],
            pydantic.Field(None, alias="schema"),
        ),
        **add_params.get("Format", {}),
    )

    class InputValue(pydantic.BaseModel):
        __root__: Union[InputValueNoObject, Dict[str, Any]]

    schema["inputValue"] = InputValue

    schema["QualifiedInputValue"] = pydantic.create_model(
        "QualifiedInputValue",
        __base__=schema["Format"],  # noqa
        value=(InputValue, ...),
        **add_params.get("QualifiedInputValue", {}),
    )

    class InlineOrRefData(pydantic.BaseModel):
        __root__: Union[
            InputValueNoObject, schema["QualifiedInputValue"], schema["Link"]  # noqa
        ]

    schema["InlineOrRefData"] = InlineOrRefData
    schema["Output"] = pydantic.create_model(
        "Output",
        __config__=ExtraAllowConfig,
        format=(Optional[schema["Format"]], None),  # noqa
        transmissionMode=(Optional[TransmissionMode], None),
        **add_params.get("Output", {}),
    )

    schema["Subscriber"] = pydantic.create_model(
        "Subscriber",
        __config__=ExtraAllowConfig,
        successUri=(Optional[pydantic.AnyUrl], None),
        inProgressUri=(Optional[pydantic.AnyUrl], None),
        failedUri=(Optional[pydantic.AnyUrl], None),
        **add_params.get("Subscriber", {}),
    )
    schema["Execute"] = pydantic.create_model(
        "Execute",
        __config__=ExtraAllowConfig,
        inputs=(
            Optional[Dict[str, Union[InlineOrRefData, List[InlineOrRefData]]]],
            None,
        ),
        outputs=(Optional[Dict[str, schema["Output"]]], None),  # noqa
        response=(Optional[Response], Response.raw),
        subscriber=(Optional[schema["Subscriber"]], None),  # noqa
        **add_params.get("Execute", {}),
    )
    schema["ProcessDescription"] = pydantic.create_model(
        "ProcessDescription",
        __base__=schema["ProcessSummary"],
        inputs=(Optional[Dict[str, schema["InputDescription"]]], None),  # noqa
        outputs=(Optional[Dict[str, schema["OutputDescription"]]], None),  # noqa
        **add_params.get("ProcessDescription", {}),
    )
    schema["StatusInfo"] = pydantic.create_model(
        "StatusInfo",
        __config__=ExtraAllowConfig,
        processID=(Optional[str], None),
        type=(JobType, ...),
        jobID=(str, ...),
        status=(StatusCode, ...),
        message=(Optional[str], None),
        created=(Optional[datetime], None),
        started=(Optional[datetime], None),
        finished=(Optional[datetime], None),
        updated=(Optional[datetime], None),
        progress=(Optional[ConInt], None),
        links=(Optional[List[schema["Link"]]], None),  # noqa
        **add_params.get("StatusInfo", {}),
    )
    schema["JobList"] = pydantic.create_model(
        "JobList",
        __config__=ExtraAllowConfig,
        jobs=(List[schema["StatusInfo"]], ...),  # noqa
        links=(List[schema["Link"]], ...),  # noqa
        **add_params.get("JobList", {}),
    )

    class Results(pydantic.BaseModel):
        __root__: Optional[Dict[str, InlineOrRefData]] = None

    schema["Results"] = Results

    schema["Exception"] = pydantic.create_model(
        "Exception",
        __config__=ExtraAllowConfig,
        type=(str, ...),
        title=(Optional[str], None),
        status=(Optional[int], None),
        detail=(Optional[str], None),
        instance=(Optional[str], None),
        **add_params.get("Exception", {}),
    )

    schema["LandingPage"] = pydantic.create_model(
        "LandingPage",
        __config__=ExtraAllowConfig,
        title=(
            Optional[str],
            pydantic.Field(default=None, example="Example processing server"),
        ),
        description=(
            Optional[str],
            pydantic.Field(
                default=None,
                example="Example server implementing the OGC API - Processes 1.0 Standard",
            ),
        ),
        links=(List[schema["Link"]], ...),  # noqa
        **add_params.get("LandingPage", {}),
    )

    return schema


schema = generate_schema()
