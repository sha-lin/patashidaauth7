from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import permissions, serializers
from rest_framework.settings import perform_import

from agriapp.permissions import IsAdminOrReadOnly
from .models import Profile, Vaccine, EmergingDisease,Growth

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

# authentication
from django.contrib.auth import authenticate, login, logout


# api
from django.http import JsonResponse
from rest_framework import status,generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import  ProfileSerializer, UserSerializer,UserCreateSerializer, VaccineSerializer,EmergingDiseaseSerializer,GrowthSerializer

# VaccineSerializer
from .permissions import IsAdminOrReadOnly


# Create your views here.

def index(request):
    return render(request, 'index.html')


# rest api ====================================

class UserList(APIView): # list all users
    """
    List all users.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserCreate(APIView): # create user
    """
    Create a user.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# login user ====================================>
class loginUser(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# logout user ====================================
class logoutUser(APIView): # logout user
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)





# ProfileList
class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# ProfileDetail
class ProfileDetail(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializers = ProfileSerializer(profile, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VaccineList(generics.ListCreateAPIView):
    querySet = Vaccine.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VaccineSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = VaccineSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_204_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': f"Vaccine {serializer.data['title']} has been created"}, status=status.HTTP_201_CREATED)
        

class VaccineDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VaccineSerializer
    Lookup_url_kwargs = 'vaccine_id'
    
    
    def get_queryset(self):
        vaccine_id = self.kwargs["pk"]
        return Vaccine.objects.filter(pk=vaccine_id)


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = VaccineSerializer(queryset, many=True)
        if len(serializer.data):
            [response] = serializer.data
        else:
            raise NotFound('The vaccine is not found',
                           code='vaccine_not_found')

        return Response(response, status=status.HTTP_200_OK)
    
    # growth=========>
class GrowthList(generics.ListCreateAPIView):
    querySet = Growth.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GrowthSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = GrowthSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_204_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': f"Growth has been created"}, status=status.HTTP_201_CREATED)
    
class GrowthDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GrowthSerializer
    Lookup_url_kwargs = 'growth_id'


# emerging disease=========>
class EmergingDiseaseList(generics.ListCreateAPIView):
    querySet = EmergingDisease.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EmergingDiseaseSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = EmergingDiseaseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_204_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': f"Disease has been created"}, status=status.HTTP_201_CREATED)
        

class EmergingDiseaseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergingDiseaseSerializer
    Lookup_url_kwargs = 'disease_id'
    
    
    # def get_queryset(self):
    #     vaccine_id = self.kwargs["pk"]
    #     return EmergingDisease.objects.filter(pk=vaccine_id)


    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = EmergingDiseaseSerializer(queryset, many=True)
    #     if len(serializer.data):
    #         [response] = serializer.data
    #     else:
    #         raise NotFound('The EmergingDetails is not found',
    #                        code='EmergingDetails_not_found')
