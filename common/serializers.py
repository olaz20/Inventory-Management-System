from rest_framework import serializers
from rest_framework import status



class BaseResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_blank=True)
    data = serializers.DictField(required=False, allow_null=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get('message'):
            representation['message'] = 'Success'
        return representation
    

class ErrorResponseSerializer(BaseResponseSerializer):
    error = serializers.DictField(required=True)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get('error'):
            representation['error'] = 'An error occurred'
        return representation