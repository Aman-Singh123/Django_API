from rest_framework import serializers
from account.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
# use for the to generate password reset token generator 
 


 
class RegistraionSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['email','name','term_condition','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
            
        }
    # here we validate the data or check the data
    def validate(self, attrs):
        password =attrs.get('password')
        password2 =attrs.get('password2')
        email=attrs.get('email')
        if password != password2 :
            raise serializers.ValidationError('password does not match ')
        # if email=='@gmail.com':
        #     raise serializers.ValidationError('email does not match  ')
            
            
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data) # create user is the function 
    
    
class UserloginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['email','password']
        
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=['id','email','name']
        
class ChangeUserPassword(serializers.Serializer):
    password=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
        
    def validate(self, attrs):
        password =attrs.get('password')
        password2 =attrs.get('password2')
        user=self.context.get('user')
        if password != password2 :
            raise serializers.ValidationError('password does not match ')
        user.set_password(password)
        user.save()
        return attrs
    
    
class SendPasswordResetEmail(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print("uid is ",uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print("token is ",token)
            link='http://localhost:3000/reset/'+uid+'/'+token
            print("link is ",link)
            return attrs
        else:
            raise ValidationErr ('you are not registered with us ')
        
        
        
# make the password reset serializer 

class UserPasswordResetSeriaizer(serializers.Serializer):
    password=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
        
    def validate(self, attrs):
        password =attrs.get('password')
        password2 =attrs.get('password2')
        uid=self.context.get('uid')
        token=self.context.get('token')
        if password != password2 :
            raise serializers.ValidationError('password does not match ')
        id=smart_str(urlsafe_base64_decode(uid))
        user=User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            return ValidationErr('token is not valid or expired')
        user.set_password(password)
        user.save()
        return attrs
    