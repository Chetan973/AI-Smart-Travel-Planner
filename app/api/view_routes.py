from fastapi import APIRouter, Path
from fastapi.responses import FileResponse

router = APIRouter(tags=["Views"])



@router.get("/checkout")
def checkout():

    return FileResponse(
        "app/templates/checkout.html"
    )

@router.get("/payment-success")
def payment_success():

    return FileResponse(
        "app/templates/payment_success.html"
    )