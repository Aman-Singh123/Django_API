from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import RegistraionSerializer,UserloginSerializer,UserProfileSerializer,ChangeUserPassword,SendPasswordResetEmail,UserPasswordResetSeriaizer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# generate tooken mannually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer=RegistraionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           user= serializer.save()
           token=get_tokens_for_user(user)
           return Response({'token':token,'msg':'registration is succesfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
 
 
 
    
class UserLoginview(APIView):
    def post(self,request,format=None):
        serializer=UserloginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login  succesfull'},status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
            
class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serialzer=UserProfileSerializer(request.user)
        return Response(serialzer.data,status=status.HTTP_200_OK)
    
    
class UserChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
       serializer=ChangeUserPassword(data=request.data,context={'user':request.user})
       if serializer.is_valid():
            return Response({'msg':'change password succesfully'},status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
   
class SendPasswordResetEmailView(APIView):
    def post(self,request,format=None):
        serializer=SendPasswordResetEmail(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset email link send'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
  
class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSeriaizer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
              return Response({'msg':'password reset Successfull '},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            