from decimal import Decimal
from typing import Annotated

from pydantic import PlainSerializer

# Se calcula con Decimal, pero en el JSON de respuesta sale como número
Money = Annotated[
    Decimal,
    PlainSerializer(lambda value: float(value), return_type=float, when_used="json"),
]