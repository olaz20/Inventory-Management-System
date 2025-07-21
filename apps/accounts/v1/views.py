from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from common.response import api_response

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return api_response(
                status_code=status.HTTP_200_OK,
                message="Login successful",
                data={
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                },
            )
        return api_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid data provided",
            data=serializer.errors,
        )