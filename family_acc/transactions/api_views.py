from . models import Currency, Account, Category, Transaction
from . forms import CreateCurrency, CreateAccount, CreateCategory, CreateExpense, CreateIncome
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . serializers import CurrencySerializer, AccountSerializer, CategorySerializer, TransactionSerializer
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
        # print(f"--DY-- data:{data}")
        form = CreateAccount(data, user=request.user)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.family = request.user.profile.family
            new_acc.save()
            return Response({"success": "account created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IncomeCreate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # fields: ["date", "account", "amount", "category", "remark"]
        data = request.data.copy()
        # get id for foreign key fields
        # data["currency"] = Currency.objects.get(code=data["currency"], family=request.user.profile.family).id
        # data["account"] = Account.objects.get(name=data["account"], family=request.user.profile.family).id
        data["category"] = Category.objects.get(name=data["category"], family=request.user.profile.family).id
        form = CreateIncome(data, user=request.user)
        if form.is_valid():
            new_inc = form.save(commit=False)
            # next should be done by signals
            # new_inc.family = request.user.profile.family
            new_inc.created_by = request.user
            new_inc.amount = abs(new_inc.amount)
            new_inc.currency = Currency.objects.get(id=new_inc.account.currency_id)
            Account.objects.filter(id=new_inc.account_id).update(balance=F('balance') + new_inc.amount)
            new_inc.save()
            return Response({"success": "income created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["category"] = Category.objects.get(name=data["category"], family=request.user.profile.family).id
        form = CreateExpense(data, user=request.user)
        if form.is_valid():
            new_exp = form.save(commit=False)
            new_exp.created_by = request.user
            new_exp.amount = -abs(new_exp.amount)
            new_exp.currency = Currency.objects.get(id=new_exp.account.currency_id)
            Account.objects.filter(id=new_exp.account_id).update(balance=F('balance') - new_exp.amount)
            new_exp.save()
            return Response({"success": "expense created"}, status=status.HTTP_201_CREATED)
        return Response(form.error, status=status.HTTP_400_BAD_REQUEST)


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
        qs = Account.objects.filter(family=family)
        print(f"--DY-- family : {family}")
        return Response(AccountSerializer(qs, many=True).data)
    

class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = Category.objects.filter(family=family)
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

        
        return Response(TransactionSerializer(qs, many=True).data)

