from . models import Currency, Account
from . forms import CreateCurrency, CreateAccount
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . serializers import CurrencySerializer, AccountSerializer

   
class CurrencyCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):        
        form = CreateCurrency(request.data)
        if form.is_valid():
            new_cur = form.save(commit=False)
            new_cur.family = request.user.profile.family
            new_cur.save()
            return Response({"success": "currency created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CurrencyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Currency.objects.filter(family=family)
        return Response(CurrencySerializer(qs, many=True).data)
    
class AccountCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        # currency is foreign key for account, to procees we need currency id in form instead of currency name(curency code)
        data["currency"] = Currency.objects.get(code=data["currency"], family=request.user.profile.family).id
        # print(f"--DY-- data:{data}")
        form = CreateAccount(data, user=request.user)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.family = request.user.profile.family
            new_acc.save()
            return Response({"success": "account created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Account.objects.filter(family=family)
        return Response(AccountSerializer(qs, many=True).data)