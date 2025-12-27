from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from baseapp.utility import *
from baseapp.email import *

#auth_validate
#create
#validate_email_phone_number

class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    auth_type = serializers.CharField(read_only = True , required = False)
    suth_status = serializers.CharField(read_only = True , required = False)
    email_phone_number = serializers.CharField(write_only = True)
    
    def __init__(self, *args , **kwargs):
        super(SignUpSerializer , self).__init__(*args , **kwargs)
        self.fields['validate_email_phone_number'] = serializers.CharField(read_only = True , required = False)
        
    class Meta:
        model = User
        fields = [
            'auth_type',
            'suth_status',
            'id',
            'email_phone_number',
        ]

    def create(self, validated_data):
       user = super(SignUpSerializer , self).create(validated_data)
       if user.auth_type == VIA_EMAIL:
           code = user.verify_code(VIA_EMAIL)
           send_email_code(user.email , code)
       elif user.auth_type == VIA_PHONE:
            code = user.verify_code(VIA_PHONE)
            pass
       else:
           data = {
               'success': 'False',
               'message' : 'Telefon raqam yoki email togri kiriting'
           }
           raise ValidationError(data)
       user.save()
       return user
           
    

    def validate(self, data):
        data = self.auth_validate(data)
        return data
    
    @staticmethod
    def auth_validate(data):
        user_input = data.get('email_phone_number')
        user_input_type = email_or_phone(user_input)

        if user_input_type == 'email':
            data = {
                'auth_type' : VIA_EMAIL,
                'email' : user_input
            }
        elif user_input == 'phone':
            data ={
                'auth_type' : VIA_PHONE,
                'phone_number' : user_input
            }
        else:

            data = {
                'success' : 'False',
                'message' : 'Telefon raqam yoki email kiriting'
            }
            raise ValidationError(data)
        
        return data
    
    def validate_email_phone_number(self , value):

        input_type = email_or_phone(value)

        if input_type not in ['email', 'phone']:
            raise ValidationError('Telefon raqam yoki email notogri')
        
        return value


