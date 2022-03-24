from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article
from rest_framework.authtoken.views import Token


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
            }
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        Token.objects.create(user=user)
        return user
