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
from typing import Any, Optional, Union

import pydantic


class Metadata(pydantic.BaseModel):
    title: Optional[str] = None
    role: Optional[str] = None
    href: Optional[str] = None


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
    rel: Optional[str] = pydantic.Field(None, example="service")
    type: Optional[str] = pydantic.Field(None, example="application/json")
    hreflang: Optional[str] = pydantic.Field(None, example="en")
    title: Optional[str] = None


class AdditionalParameters(Metadata):
    parameters: Optional[list[AdditionalParameter]] = None


class DescriptionType(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[list[str]] = None
    metadata: Optional[list[Metadata]] = None
    additionalParameters: Optional[AdditionalParameters] = None


class ProcessSummary(DescriptionType):
    id: str
    version: str
    jobControlOptions: Optional[list[JobControlOptions]] = None
    outputTransmission: Optional[list[TransmissionMode]] = None
    links: Optional[list[Link]] = None


class ProcessesList(pydantic.BaseModel):
    processes: list[ProcessSummary]
    links: list[Link]
