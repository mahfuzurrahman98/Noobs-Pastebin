from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class createUserSchema(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str

    @validator('name', 'username')
    def validate_blank_fields(cls, value, field):
        field_name = field.alias
        value = value.strip()
        if value == '':
            raise ValueError(f'{field_name.capitalize()} cannot be blank')
        return value

    @validator('password')
    def validate_password(cls, value):
        value = value.strip()
        if ' ' in value:
            raise ValueError('Password cannot contain spaces')
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters')
        return value


class updateUserSchema(BaseModel):
    name: Optional[str]

    @validator('name')
    def validate_blank_fields(cls, value, field):
        field_name = field.alias
        value = value.strip() if field_name != 'lnaguage' else value
        if value == '':
            raise ValueError(f'{field_name.capitalize()} cannot be blank')
        return value

    @validator('name')
    def validate_name(cls, value):
        if value and not value.strip():
            raise ValueError('Name cannot be blank if provided')
        return value
