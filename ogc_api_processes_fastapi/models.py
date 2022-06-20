from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    title: Optional[str] = None
    role: Optional[str] = None
    href: Optional[str] = None


class AdditionalParameter(BaseModel):
    name: str
    value: list[Union[str, float, int, list[Any], dict[str, Any]]]


class JobControlOptions(Enum):
    sync_execute: str = "sync-execute"
    async_execute: str = "async-execute"
    dismiss: str = "dismiss"


class TransmissionMode(Enum):
    value: str = "value"
    reference: str = "reference"


class Link(BaseModel):
    href: str
    rel: Optional[str] = Field(None, example="service")
    type: Optional[str] = Field(None, example="application/json")
    hreflang: Optional[str] = Field(None, example="en")
    title: Optional[str] = None


class AdditionalParameters(Metadata):
    parameters: Optional[list[AdditionalParameter]] = None


class DescriptionType(BaseModel):
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


class ProcessesList(BaseModel):
    processes: list[ProcessSummary]
    links: list[Link]
