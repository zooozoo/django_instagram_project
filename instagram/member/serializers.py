from rest_framework import serializers
from rest_framework.authtoken.models import Token

from member.forms import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'age',
        )


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'password1',
            'password2',
            'age',
            'token',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            img_profile=validated_data['img_profile'],
            age=validated_data['age'],
        )

    def get_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key
        # return Token.objects.create(user=obj).key 이것도 가능

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'user': ret,
            'token': instance.token,
        }
        return data
