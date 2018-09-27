from django.http import JsonResponse

def login_required_response():
    return JsonResponse({
        "message": "User unauthorized",
    }, status=401)