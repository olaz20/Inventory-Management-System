from rest_framework import status
from rest_framework.response import Response
from .serializers import BaseResponseSerializer

def api_response(message="Success", data=None, status_code=status.HTTP_200_OK):
    serializer = BaseResponseSerializer(data={
        "message": message,
        "data": data,
    })
    serializer.is_valid()
    return Response(serializer.data, status=status_code)
