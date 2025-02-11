"""
Definition of the :class:`ExportDestinationViewSet` class.
"""
from accounts.filters import ExportDestinationFilter
from accounts.models.export_destination import ExportDestination
from accounts.serializers.export_destination import ExportDestinationSerializer
from accounts.tasks import export_mri_scan, export_mri_session, export_run
from django.db.models import QuerySet
from paramiko import SSHException
from pylabber.views.defaults import DefaultsMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

EXPORT_HANDLERS: dict = {
    "django_mri": {"Session": export_mri_session, "Scan": export_mri_scan},
    "django_analyses": {"Run": export_run},
}


class ExportDestinationViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows
    :class:`~accounts.models.export_destination.ExportDestination` instances to
    be viewed or edited.
    """

    queryset = ExportDestination.objects.order_by("id")
    serializer_class = ExportDestinationSerializer
    filter_class = ExportDestinationFilter

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        user = self.request.user
        queryset = super().filter_queryset(queryset)
        return queryset.filter(users=user)

    @action(detail=False, methods=["POST"])
    def export_instance(
        self, request: Request,
    ):
        try:
            app_label = request.data.pop("app_label")
            model_name = request.data.pop("model_name")
            export_destination_id = request.data.pop("export_destination_id")
            instance_id = request.data.pop("instance_id")
        except KeyError:
            return Response(status.HTTP_400_BAD_REQUEST)
        handler = EXPORT_HANDLERS.get(app_label, {}).get(model_name)
        if handler:
            try:
                handler.delay(
                    export_destination_id, instance_id, **self.request.data
                )
            except AttributeError:
                handler(
                    export_destination_id, instance_id, **self.request.data
                )
            finally:
                return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def get_status(self, request: Request, pk: int):
        export_destination = ExportDestination.objects.get(id=pk)
        try:
            export_destination.sftp_client
        except (RuntimeError, SSHException, ConnectionResetError):
            status = False
        else:
            status = True
        return Response(data=status)
