from django.http import JsonResponse
from django.http.response import Http404
from rest_framework import status
from django.http import HttpResponseServerError
from django.utils.deprecation import MiddlewareMixin
import jwt
jwtSecret = "KWNMRDPOUC"


class AuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.get_full_path()
        if url not in ['/user/login', '/user/register', '/admin/advisor']:
            if 'Authorization' in request.headers.keys():
                try:
                    token = request.headers['Authorization']
                    jwt.decode(token, jwtSecret, algorithms=["HS256"])
                except jwt.ExpiredSignatureError:
                    return JsonResponse(
                        {"success": False, "reason":  "Expired Token"}, status=status.HTTP_401_UNAUTHORIZED)
                except jwt.InvalidSignatureError:
                    return JsonResponse(
                        {"success": False, "reason": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        return self.get_response(request)

    # def process_request(self, request):
        # return Http404

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        return response
