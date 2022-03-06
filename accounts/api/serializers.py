from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions


class UserSerializer(serializers.HyperlinkedModelSerializer):
# 同时验证用户的输入，serializer的功能: 1. 序列化 2. 验证用户的输入
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class UserSerializerForTweets(serializers.HyperlinkedModelSerializer):
# 同时验证用户的输入，serializer的功能: 1. 序列化 2. 验证用户的输入
    class Meta:
        model = User
        fields = ('id', 'username')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs['username'].lower()
        if not User.objects.filter(username=username).exists():
            raise exceptions.ValidationError({'username': 'User does not exists.'})
        attrs['username'] = username
        return attrs

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, data):
        # TODO<HOMEWORK> 增加验证 username 是不是只由给定的字符集合构成
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email address has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user

    