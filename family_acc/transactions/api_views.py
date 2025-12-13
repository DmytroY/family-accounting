from . models import Currency
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CurrencyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Currency.objects.filter(family=family)
        from . serializers import CurrencySerializer
        return Response(CurrencySerializer(qs, many=True).data)