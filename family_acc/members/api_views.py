from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class MemberList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        family = request.user.profile.family
        qs = User.objects.filter(profile__family=family)
        from .serializers import MemberSerializer
        return Response(MemberSerializer(qs, many=True).data)