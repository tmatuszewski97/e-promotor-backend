from rest_framework import generics
from core.api.serializers import file as fileSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsNotStudent, IsCreatorOfFile
from rest_framework.response import Response
from core.models import File
from django.db.models.query_utils import Q


# # Views associated with File model


class FileAdd(generics.CreateAPIView):
    serializer_class = fileSerializers.FileAddSerializer
    permission_classes = (IsAuthenticated & IsNotStudent,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=self.request.user)

        return Response({
            'message': "Successfully added a file on server",
            'file': serializer.data
        })


class FileList(generics.ListAPIView):
    serializer_class = fileSerializers.FileUserForGetSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        # If user is an administrator, he is able to see all files
        if (user.role == 1):
            return File.objects.all().order_by('creation_date')
        else:
            # If not - user see only files, which he created or which are shared for him
            return File.objects.filter(Q(creator=user) | Q(shared_for=user.role)).order_by('creation_date')


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return fileSerializers.FileUserForGetSerializer
        else:
            return fileSerializers.FileUserForUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Everyone who is logged in are able to see file details
            return [IsAuthenticated(), ]
        else:
            # Only logged users with administrator, dean_worker or promotor role can change informations about created (by yourself) file
            return [IsAuthenticated(), IsNotStudent(), IsCreatorOfFile(), ]
    # permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        # If user is an administrator, he is able to see all files
        if (user.role == 1):
            return File.objects.all()
        else:
            # If not - user see only files, which he created or which are shared for him
            return File.objects.filter(Q(creator=user) | Q(shared_for=user.role))
