from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.payment_schemas import (
    CreatePaymentOrderRequest,
    CreatePaymentOrderResponse,
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from app.database import get_db
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"]
)


@router.post(
    "/create-order",
    response_model=CreatePaymentOrderResponse
)
def create_payment_order(
    request: CreatePaymentOrderRequest,
    db: Session = Depends(get_db)
):

    try:

        return PaymentService.create_order(
            db,
            request
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
    
@router.post(
    "/verify",
    response_model=VerifyPaymentResponse
)
def verify_payment(
    request: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):

    try:

        return PaymentService.verify_payment(
            db,
            request
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )