from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import secrets
from .forms import RegisterForm
from rest_framework import status

class MemberList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = User.objects.filter(profile__family=family)
        from .serializers import MemberSerializer
        return Response(MemberSerializer(qs, many=True).data)
    
class RegisterAPIView(APIView):
    authentication_classes = []   # public endpoint
    permission_classes = []

    def post(self, request):
        family_token = secrets.token_urlsafe(16)
        print(f"--DY-- family_token:{family_token}")

        form = RegisterForm(request.data, family_token=family_token)
        if form.is_valid():
            user = form.save()
            user.profile.family = family_token
            user.profile.save()
            return Response({"success": "user created"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)