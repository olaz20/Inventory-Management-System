from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    serilializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return self.action_response(
                status=status.HTTP_200_OK,
                message="Login successful",
                data={
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                },
            )
        return self.action_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Invalid data provided",
            data=serializer.errors,
        )