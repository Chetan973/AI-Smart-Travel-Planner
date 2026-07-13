from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
import traceback

from app.api.schemas import (
    UserInitializationRequest,
    UserInitializationResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
)
from app.database import get_db
from app.services.user_service import UserService
from app.services.otp_service import OTPService

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.post(
    "/init",
    response_model=UserInitializationResponse,
    summary="Get Existing User or Create New User"
)
def initialize_user(
    request: UserInitializationRequest,
    db: Session = Depends(get_db)
):
    """
    Initialize User

    - Returns existing user if email already exists.
    - Updates user details if name/mobile changed.
    - Creates a new user if email is not registered.
    """

    try:

        user = UserService.get_or_create_user(
            db=db,
            request=request
        )

        OTPService.generate_and_send(
            db=db,
            user=user
        )

        return user

    except Exception as ex:

        traceback.print_exc()

        print("=" * 80)
        print(type(ex))
        print(ex)
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
            )
    

@router.post(
    "/verify-otp",
    response_model=VerifyOTPResponse,
    summary="Verify Email OTP"
)
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    try:

        OTPService.verify_otp(
            db=db,
            email=request.email,
            otp=request.otp
        )

        return VerifyOTPResponse(
            message="OTP Verified Successfully",
            email_verified=True
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

    except Exception as ex:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )