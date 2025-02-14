import base64
from decimal import Decimal

from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import PlainValidator
from typing import Annotated, Any

# Declare customized float type
Float = Annotated[
    # Note: Before decimalization, apply str() to keep the precision
    float,
    PlainSerializer(lambda v: Decimal(str(v)), return_type=Decimal),
]


def decode_base64_string(value: Any) -> bytes:
    if type(value) == bytes:
        return value

    elif type(value) == str:
        return base64.b64decode(value)

    else:
        raise ValueError(f"Invalid value type: {type(value)}")


Base64EncodedBytes = Annotated[
    bytes,
    PlainValidator(
        func=decode_base64_string,
        json_schema_input_type=str,
    ),
    PlainSerializer(
        func=lambda v: base64.b64encode(v).decode().strip(),
        return_type=str,
    ),
]
