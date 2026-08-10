from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """
    Simple liveness check. Used to confirm the API is running —
    later this can be extended to check DB connectivity too.
    """
    return {"status": "ok", "service": "soc-platform-backend"}