# Copyright (c) 2018 Ultimaker B.V.
from typing import Optional


class BaseModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Authentication data template.
class AuthenticationResponse(BaseModel):
    """Data comes from the token response with success flag and error message added."""
    success = True  # type: bool
    token_type = None  # type: Optional[str]
    access_token = None  # type: Optional[str]
    refresh_token = None  # type: Optional[str]
    expires_in = None  # type: Optional[str]
    scope = None  # type: Optional[str]
    err_message = None  # type: Optional[str]


# Response status template.
class ResponseStatus(BaseModel):
    code = 200  # type: int
    message = ""  # type str


# Response data template.
class ResponseData(BaseModel):
    status = None  # type: Optional[ResponseStatus]
    data_stream = None  # type: bytes
    content_type = "text_html"  # type: str


# Possible HTTP responses.
HTTP_STATUS = {
    "OK": ResponseStatus(code=200, message="OK"),
    "NOT_FOUND": ResponseStatus(code=404, message="NOT FOUND")
}
