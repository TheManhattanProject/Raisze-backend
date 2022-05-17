
from rest_framework import generics,status
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS

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
    
class UpdateToolsView(generics.UpdateAPIView):
    queryset = Tools.objects.all()
    serializer_class = CreateToolsSerializer
    permission_classes = (IsAdminUser,)
    # authentication_classes = []

class ListToolsView(generics.ListAPIView):
    queryset = Tools.objects.all()
    serializer_class = CreateToolsSerializer
    permission_classes = []
    authentication_classes = []
