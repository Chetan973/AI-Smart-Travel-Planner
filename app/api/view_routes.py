from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Views"])


@router.get("/checkout")
def checkout():

    return FileResponse(
        "app/templates/checkout.html"
    )