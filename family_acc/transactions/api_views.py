from . models import Currency
from . forms import CreateCurrency
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class CurrencyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Currency.objects.filter(family=family)
        from . serializers import CurrencySerializer
        return Response(CurrencySerializer(qs, many=True).data)
    
class CurrencyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = CreateCurrency(request.data)
        if form.is_valid():
            new_cur = form.save()
            new_cur.family = request.user.profile.family
            new_cur.save()
            return Response({"success": "currency created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)