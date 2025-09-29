import datetime
from typing import Optional

from services.api.common.schemas import CamelCaseModel


class TokenUser(CamelCaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    last_login: Optional[datetime.datetime] = None
    date_joined: Optional[datetime.datetime] = None
