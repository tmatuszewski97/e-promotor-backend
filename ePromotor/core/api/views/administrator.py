from rest_framework import generics
from core.api.serializers import user as userSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsAdministrator
from rest_framework.response import Response
from core.models import User


# Views associated with User model with administrator role


class AdministratorRegister(generics.CreateAPIView):
    serializer_class = userSerializer.UserRegisterSerializer
    permission_classes = (IsAuthenticated & IsAdministrator,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(new_role=1, is_staff=True)
        return Response({
            'message': "Successfully registered an administrator",
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
        })


class AdministratorList(generics.ListAPIView):
    serializer_class = userSerializer.UserListSerializer
    permission_classes = (IsAuthenticated & IsAdministrator,)
    # permission_classes = [AllowAny]
    queryset = User.objects.filter(role=1).order_by('first_name', 'last_name')


class AdministratorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = userSerializer.UserDetailForAdminAndDeanWorkerSerializer
    permission_classes = (IsAuthenticated & IsAdministrator,)
    # permission_classes = [AllowAny]
    queryset = User.objects.all()
