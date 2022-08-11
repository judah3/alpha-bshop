from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from account.models import UserProfile
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer, UserListSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
# Create your views here.

@api_view(['get'])
def searchCustomer(request):
    search = UserProfile.objects.all().filter(firstname__icontains=request.data.get('search'),role='Customer')
    serializer = UserListSerializer(search, many=True)
    return Response(serializer.data)

@api_view(['get'])
def customerList(request):
    customer_list = UserProfile.objects.all().filter(role='Customer')
    serializer = UserListSerializer(customer_list, many=True)
    return Response(serializer.data)

@api_view(['get'])
def customerDetail(request, id):
    customer_details = UserProfile.objects.get(id = id)
    serializer = UserListSerializer(customer_details)
    return Response(serializer.data, status=status.HTTP_200_OK)
            

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.validated_data['user']
      
        login(request, new_user)
        return super(LoginAPI, self).post(request, format=None)

class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        profile = {
            'user': user.id,
            'firstname': request.data.get('firstname'),
            'lastname': request.data.get('lastname'),
            'role': request.data.get('role'),
        }

        profile_serializer = UserProfileSerializer(data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile = profile_serializer.save(user=user)

        
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "profile": UserProfileSerializer(profile, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

