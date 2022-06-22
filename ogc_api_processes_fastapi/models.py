import enum
import typing as T

import pydantic


class Metadata(pydantic.BaseModel):
    title: T.Optional[str] = None
    role: T.Optional[str] = None
    href: T.Optional[str] = None


class AdditionalParameter(pydantic.BaseModel):
    name: str
    value: list[T.Union[str, float, int, list[T.Any], dict[str, T.Any]]]


class JobControlOptions(enum.Enum):
    sync_execute: str = "sync-execute"
    async_execute: str = "async-execute"
    dismiss: str = "dismiss"


class TransmissionMode(enum.Enum):
    value: str = "value"
    reference: str = "reference"


class Link(pydantic.BaseModel):
    href: str
    rel: T.Optional[str] = pydantic.Field(None, example="service")
    type: T.Optional[str] = pydantic.Field(None, example="application/json")
    hreflang: T.Optional[str] = pydantic.Field(None, example="en")
    title: T.Optional[str] = None


class AdditionalParameters(Metadata):
    parameters: T.Optional[list[AdditionalParameter]] = None


class DescriptionType(pydantic.BaseModel):
    title: T.Optional[str] = None
    description: T.Optional[str] = None
    keywords: T.Optional[list[str]] = None
    metadata: T.Optional[list[Metadata]] = None
    additionalParameters: T.Optional[AdditionalParameters] = None


class ProcessSummary(DescriptionType):
    id: str
    version: str
    jobControlOptions: T.Optional[list[JobControlOptions]] = None
    outputTransmission: T.Optional[list[TransmissionMode]] = None
    links: T.Optional[list[Link]] = None


class ProcessesList(pydantic.BaseModel):
    processes: list[ProcessSummary]
    links: list[Link]
