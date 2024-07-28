from pydantic import BaseModel, AnyHttpUrl


class URLBaseSchema(BaseModel):
    target_url: AnyHttpUrl


class URLSchema(URLBaseSchema):
    is_active: bool
    clicks: int


class URLInfoSchema(URLSchema):
    url: str
    admin_url: str


class URLAddSchema(BaseModel):
    target_url: str
    key: str
    secret_key: str
