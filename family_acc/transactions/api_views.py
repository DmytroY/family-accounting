from . models import Currency, Account, Category, Transaction
from . forms import CreateCurrency, CreateAccount, CreateCategory, CreateExpense, CreateIncome
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . serializers import CurrencySerializer, AccountSerializer, CategorySerializer, TransactionSerializer, TransactionCreateSerializer
from django.db.models import F

   
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
    

class AccountCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        # currency is foreign key for account, to procees we need currency id in form instead of currency name(curency code)
        data["currency"] = Currency.objects.get(code=data["currency"], family=request.user.profile.family).id
        form = CreateAccount(data, user=request.user)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.family = request.user.profile.family
            new_acc.save()
            return Response({"success": "account created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TransactionCreate(APIView):
    permission_classes = [IsAuthenticated]
    trx_type = None
    
    def post(self, request):
        serializer = TransactionCreateSerializer(
            data = request.data,
            context={'request': request, 'transaction_type': self.trx_type}
        )
        serializer.is_valid(raise_exception=True)
        trx = serializer.save()
        Account.objects.filter(id=trx.account_id).update(balance=F('balance') + trx.amount)
        return Response({"success": "transaction created"}, status=status.HTTP_201_CREATED)


class CategoryCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = CreateCategory(request.data)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.family = request.user.profile.family
            new_cat.save()
            return Response({"success": "category created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrencyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Currency.objects.filter(family=family)
        return Response(CurrencySerializer(qs, many=True).data)
    
class AccountList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        currency_id = request.query_params.get("currency_id")
        qs = Account.objects.filter(family=family)
        if currency_id:
            qs = qs.filter(currency=currency_id)
        return Response(AccountSerializer(qs, many=True).data)
    
def str_to_bool(str) -> bool:
    return str.lower() in ("1", "true", "yes")

class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        income_flag = request.query_params.get("income_flag") # true
        expense_flag = request.query_params.get("expense_flag") # false
        qs = Category.objects.filter(family=family)

        if income_flag is not None:
            qs = qs.filter(income_flag=str_to_bool(income_flag))
        if expense_flag is not None:
            qs = qs.filter(expense_flag=str_to_bool(expense_flag))

        return Response(CategorySerializer(qs, many=True).data)
    
class TransactionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Transaction.objects.filter(family=family)
        date_from = request.query_params.get("from")
        date_to = request.query_params.get("to")
        account_id = request.query_params.get("account_id")
        account_name = request.query_params.get("account")
        category_name = request.query_params.get("category")
        currency_code = request.query_params.get("currency")
        count = request.query_params.get("count")

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if account_id:
            qs = qs.filter(account=account_id)
        if account_name:
            qs = qs.filter(account__name=account_name, category__family=family)
        if category_name:
            qs = qs.filter(category__name=category_name, category__family=family)
        if currency_code:
             qs = qs.filter(currency__code=currency_code, currency__family=family)
        if count:
            qs = qs.order_by("-date", "-id")[:int(count)]

        return Response(TransactionSerializer(qs, many=True).data)

