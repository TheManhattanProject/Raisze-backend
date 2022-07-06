
from django.forms import ValidationError
from django.http import Http404
from rest_framework import generics,status
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from .models import Valuation
from .models import Tools
from .serializers import CreateValuationSerializer
from .serializers import CreateToolsSerializer

# Create your views here.

class CreateValuationView(generics.CreateAPIView):
    serializer_class = CreateValuationSerializer
    query_set = Valuation.objects.all()
    permission_classes = []
    authentication_classes = []


class CreateToolsView(generics.CreateAPIView):
    queryset = Tools.objects.all()
    serializer_class = CreateToolsSerializer
    permission_classes = (IsAdminUser,)
    # authentication_classes = []
    
class UpdateToolsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateToolsSerializer
    permission_classes = (IsAdminUser,)
    # authentication_classes = []

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Tools.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Tool id was not passed in the url")
        if activity.exists():
            activity[0].clicks += 1
            activity[0].save()
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListToolsView(generics.ListAPIView):
    queryset = Tools.objects.filter(is_deleted=False)
    serializer_class = CreateToolsSerializer
    permission_classes = []
    authentication_classes = []
