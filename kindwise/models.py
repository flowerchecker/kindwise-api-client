from dataclasses import dataclass
from datetime import datetime


@dataclass
class SimilarImage:
    id: str
    url: str
    similarity: float
    url_small: str
    license_name: str | None = None
    license_url: str | None = None
    citation: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'SimilarImage':
        return cls(
            id=data['id'],
            url=data['url'],
            similarity=data['similarity'],
            url_small=data['url_small'],
            license_name=data.get('license_name'),
            license_url=data.get('license_url'),
            citation=data.get('citation'),
        )


@dataclass
class Suggestion:
    id: str
    name: str
    probability: float
    similar_images: list[SimilarImage] | None = None
    details: dict | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Suggestion':
        return cls(
            id=data['id'],
            name=data['name'],
            probability=data['probability'],
            similar_images=None
            if data.get('similar_images') is None
            else [SimilarImage.from_dict(similar_image) for similar_image in data['similar_images']],
            details=data.get('details'),
        )


@dataclass
class Classification:
    suggestions: list[Suggestion]

    @classmethod
    def from_dict(cls, data: dict) -> 'Classification':
        return cls(suggestions=[Suggestion.from_dict(suggestion) for suggestion in data['suggestions']])


@dataclass
class Result:
    classification: Classification

    @classmethod
    def from_dict(cls, data: dict) -> 'Result':
        return cls(classification=Classification.from_dict(data['classification']))


@dataclass
class Input:
    images: list[str]
    datetime: datetime
    latitude: float | None
    longitude: float | None
    similar_images: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'Input':
        return cls(
            images=data['images'],
            datetime=datetime.fromisoformat(data['datetime']),
            latitude=data['latitude'],
            longitude=data['longitude'],
            similar_images=data['similar_images'],
        )


@dataclass
class Identification:
    access_token: str
    model_version: str
    custom_id: str | None
    input: Input
    result: Result
    status: str
    sla_compliant_client: bool
    sla_compliant_system: bool
    created: datetime
    completed: datetime

    @classmethod
    def from_dict(cls, data: dict) -> 'Identification':
        return cls(
            access_token=data['access_token'],
            model_version=data['model_version'],
            custom_id=data['custom_id'],
            input=Input.from_dict(data['input']),
            result=Result.from_dict(data['result']),
            status=data['status'],
            sla_compliant_client=data['sla_compliant_client'],
            sla_compliant_system=data['sla_compliant_system'],
            created=datetime.fromtimestamp(data['created']),
            completed=datetime.fromtimestamp(data['completed']),
        )


@dataclass
class Limits:
    day: int | None
    week: int | None
    month: int | None
    total: int | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            day=data['day'],
            week=data['week'],
            month=data['month'],
            total=data['total'],
        )


@dataclass
class CanUseCredits:
    value: bool
    reason: str | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            value=data['value'],
            reason=data['reason'],
        )


@dataclass
class UsageInfo:
    active: bool
    credit_limits: Limits
    used: Limits
    can_use_credits: CanUseCredits
    remaining: Limits

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            active=data['active'],
            credit_limits=Limits.from_dict(data['credit_limits']),
            used=Limits.from_dict(data['used']),
            can_use_credits=CanUseCredits.from_dict(data['can_use_credits']),
            remaining=Limits.from_dict(data['remaining']),
        )
