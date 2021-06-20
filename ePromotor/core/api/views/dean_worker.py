from rest_framework import generics
from core.api.serializers import dean_worker as deanWorkerSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsAdministrator, IsAdministratorOrDeanWorker
from rest_framework.response import Response
from core.models import DeanWorker


# Views associated with User model with dean worker role


class DeanWorkerRegister(generics.CreateAPIView):
    serializer_class = deanWorkerSerializers.DeanWorkerRegisterSerializer
    permission_classes = (IsAuthenticated & IsAdministrator,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': "Successfully registered a dean worker",
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
        })


class DeanWorkerList(generics.ListAPIView):
    serializer_class = deanWorkerSerializers.DeanWorkerUserListSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]
    queryset = DeanWorker.objects.all().order_by(
        'user__first_name', 'user__last_name')


class DeanWorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = deanWorkerSerializers.DeanWorkerUserDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdministratorOrDeanWorker(), ]
        else:
            return [IsAuthenticated(), IsAdministrator(), ]
    # permission_classes = [AllowAny]

    queryset = DeanWorker.objects.all()
