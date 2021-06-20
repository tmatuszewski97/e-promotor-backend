from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from core.api.serializers import user as userSerializers
from core.api.serializers import dean_worker as deanWorkerSerializers
from core.api.serializers import promoter as promoterSerializers
from core.api.serializers import student as studentSerializers
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsNotStudent
from core.models import User, DeanWorker, Promoter, Student


# Views associated with User model


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': "You are logged successfully",
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
            'token': token.key
        })


class UserChangePassword(generics.UpdateAPIView):
    serializer_class = userSerializers.UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.validated_data['password'])
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)
        user.save()

        return Response({
            'message': "Your password has been changed",
            # 'token': token.key
        })

    # Changing password is enabled only for logged user account
    def get_object(self):
        return User.objects.get(id=self.request.user.id)


class UserDetail(generics.RetrieveUpdateAPIView):

    # Serializer is choosing based on role of logged user
    def get_serializer_class(self):
        if self.request.user.role == 1:
            # User with administrator role can deactivate account by setting "active" to false
            return userSerializers.UserDetailSerializer
        elif self.request.user.role == 2:
            return deanWorkerSerializers.DeanWorkerUserDetailSerializer
        elif self.request.user.role == 3:
            return promoterSerializers.PromoterUserDetailSerializer
        elif self.request.user.role == 4:
            return studentSerializers.StudentUserDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Everyone who is logged in are able to see account details
            return [IsAuthenticated(), ]
        else:
            # Only logged users with administrator, dean_worker or promoter role can change informations about account
            return [IsAuthenticated(), IsNotStudent(), ]
    # permission_classes = [AllowAny]

    # Queryset is choosing based on role of logged user
    def get_object(self):
        if self.request.user.role == 1:
            return User.objects.get(id=self.request.user.id)
        elif self.request.user.role == 2:
            return DeanWorker.objects.get(user=self.request.user)
        elif self.request.user.role == 3:
            return Promoter.objects.get(user=self.request.user)
        elif self.request.user.role == 4:
            return Student.objects.get(user=self.request.user)
