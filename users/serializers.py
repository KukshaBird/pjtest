from rest_framework import serializers
from .models import User, Statistic

class UserSerializer(serializers.Serializer):

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    gender = serializers.ChoiceField(choices=User.GENDER)
    ip_address = serializers.IPAddressField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class StatisticSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    date = serializers.DateField()
    page_views = serializers.IntegerField()
    clicks = serializers.IntegerField()

    def create(self, validated_data):
        return Statistic.objects.get_or_create(**validated_data)
