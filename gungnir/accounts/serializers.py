from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError
)
from dataCollector.models import Topics_model

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    # email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            # 'email2',
            'password',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

    # def validate_email(self, value):
    #     data = self.get_initial()
    #     email1 = data.get("email2")
    #     email2 = value
    #     if email1 != email2:
    #         raise ValidationError("Emails must match.")
    #
    #     user_qs = User.objects.filter(email=email2)
    #     if user_qs.exists():
    #         raise ValidationError("This user has already registered.")
    #
    #     return value
    #
    # def validate_email2(self, value):
    #     data = self.get_initial()
    #     email1 = data.get("email")
    #     email2 = value
    #     if email1 != email2:
    #         raise ValidationError("Emails must match.")
    #     return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    #email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            # 'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        username = data.get("username",None)
        print(username)
        #email = data.get("email",None)
        password = data["password"]
        if not username:
            raise ValidationError("A username is required to login")
        user = User.objects.filter(Q(username = username) ).distinct()
        #user = user.exclude(email__isnull = True).exclude(email__iexact = '')
        print(user.first().email)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
            print(user_obj)
        else:
            raise ValidationError("Not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect")
        return data

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "first_name",
            "last_name",
            "collection_topic_id_array"
        ]
        read_only_fields = ("username", "email", "date_joined")


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "date_joined",
            "first_name",
            "last_name",
            "collection_topic_id_array",
        ]
        read_only_fields = ("username","email","date_joined")

    def validate(self, data):
        firstname = data.get("first_name",None)
        username = data.get("username",None)
        return data
