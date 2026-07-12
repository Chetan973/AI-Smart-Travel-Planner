from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserRegistrationRequest(BaseModel):

    full_name: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    mobile_no: str = Field(
        min_length=10,
        max_length=10
    )


class UserResponse(BaseModel):

    user_id: int

    full_name: str

    email: EmailStr

    mobile_no: str

    email_verified: bool

    model_config = {
        "from_attributes": True
    }