# app/api/payment_routes.py
import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

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

# Schema for the Demo Bypass Request
class DemoBypassRequest(BaseModel):
    booking_reference: str
    email: str

@router.post(
    "/create-order",
    response_model=CreatePaymentOrderResponse
)
def create_payment_order(
    request: CreatePaymentOrderRequest,
    db: Session = Depends(get_db)
):
    try:
        return PaymentService.create_order(db, request)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post(
    "/verify",
    response_model=VerifyPaymentResponse
)
def verify_payment(
    request: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):
    try:
        return PaymentService.verify_payment(db, request)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/status/{booking_reference}", response_model=VerifyPaymentResponse)
def payment_status(booking_reference: str, db: Session = Depends(get_db)):
    try:
        return PaymentService.get_status(db, booking_reference)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex)) from ex

@router.post("/demo-bypass", summary="Bypass Payment for Demo Mode")
def demo_bypass_payment(request: DemoBypassRequest, db: Session = Depends(get_db)):
    """
    Allows skipping Razorpay during live presentations if DEMO_MODE_ENABLED=True.
    """
    try:
        # Call the new bypass method we created in PaymentService
        result = PaymentService.process_demo_bypass(db, request.booking_reference)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error during demo bypass.")