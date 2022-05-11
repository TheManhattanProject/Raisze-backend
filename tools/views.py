
from rest_framework import generics,status
from .models import Valuation
from .serializers import CreateValuationSerializer

# Create your views here.

class CreateValuationView(generics.CreateAPIView):
    serializer_class = CreateValuationSerializer
    query_set = Valuation.objects.all()
    permission_classes = []
    authentication_classes = []


