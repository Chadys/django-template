from common.routers import FixRouter

router = FixRouter()


@router.get("/health_check")
def health_check(request):
    return {}
