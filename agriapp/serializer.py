from rest_framework import serializers


from .models import Profile,Vaccine,EmergingDisease,Growth

# cloudinary
from cloudinary.models import CloudinaryField
# user
from django.contrib.auth.models import User


# get all users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','date_joined')

# create user
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user_name", "parent_name", "place of birth", "contact", "location", "address", "DoB", "updated_at")

class VaccineSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    class Meta:
        model = Vaccine
        fields = ['title', 'vaccine_name', 'batch_number', 'drug_expiry', 'next_appointment','user_profile'] 
        
         
        # growth======
class GrowthSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    class Meta:
        model = Growth
        fields = ['patient','patient_name','age', 'weight', 'height', 'HO','date']     
    
    
    # emerging disease====
class EmergingDiseaseSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    class Meta:
        model = EmergingDisease
        fields = ['disease_name', 'patient']   