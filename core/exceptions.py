from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # DRF handled errors (ValidationError etc.)
    if response is not None:
        return response

    # Your service layer errors
    if isinstance(exc, ValueError):
        return Response(
            {"error": str(exc)},
            status=400
        )

    # fallback
    return Response(
        {"error": "Something went wrong"},
        status=500
    )