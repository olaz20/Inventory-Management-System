from rest_framework import APIView
from  rest_framework import status
from .response import api_response
from .permission import IsSuperuser
from .tasks import generate_inventory_report
from celery.result import AsyncResult
import os
from django.http import FileResponse
from django.conf import settings
import logging


logging = logging.getLogger(__name__)

class ReportStatusView(APIView):
    permission_classes = [IsSuperuser]

    def get(self, request, task_id):
        try: 
            task = AsyncResult(task_id)
            if task.state == 'PENDING':
                return api_response(
                    message="Report generation in progress",
                    data={"task_id": task_id, "status": "pending"},
                    status=status.HTTP_202_ACCEPTED)
            elif task.state == 'SUCCESS':
                result = task.result
                if result['status'] == 'completed':
                    return api_response(
                        message="Report generated successfully",
                        data={
                            "task_id": task_id,
                            "status": "completed",
                            "inventory_file": os.path.basename(result['inventory_file']),
                            "supplier_file": os.path.basename(result['supplier_file'])
                        },
                        status=status.HTTP_200_OK)
                else:
                    return api_response(
                        message="Report generation failed",
                        data={"details": result["message"]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return api_response(
                    message="Report generation failed  or unknown state",
                    data={"detail": task.state},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"Error checking report status {task_id} : {str(e)}")
            return api_response(
                message="Failed to check report status",
                data={"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadReportView(APIView):
    permission_classes = [IsSuperuser]

    def get(self, request, filename):
        try:
            file_path = os.path.join(settings.BASE_DIR, 'reports', filename)
            if not os.path.exists(file_path):
                logging.warning(f"Report file not found: {filename}")
                return api_response(
                    message="Report file not found",
                    errors={'detail': 'File does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            logging.info(f"Report downloaded: {filename} by {request.user.username}")
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        except Exception as e:
            logging.error(f"Error downloading report {filename}: {str(e)}")
            return api_response(
                message="Failed to download report",
                errors={'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )