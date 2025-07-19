from rest_framework.permissions import BasePermission
import logging

logging = logging.getLogger(__name__)
class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        try:
            is_superuser = request.user and request.user.is_superuser and request.user.is_authenticated
            if not is_superuser:
                logging.warning(f"Access denied for user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
            else:
                logging.info(f"Access granted for superuser: {request.user.username}")
            return is_superuser
        except Exception as e:
            logging.error(f"Error checking superuser permission: {str(e)}")
            return False