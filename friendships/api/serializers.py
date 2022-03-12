from accounts.api.serializers import UserSerializer
from friendships.models import Friendship
from rest_framework import serializers


# 可以通过 source=xxx 指定去访问每个model instance 的xxx方法
# 即 model_instance.xxx 来获得数据
# https://www.django-rest-framework.org/api-guide/serialziers/#specifying-fields-explicityly
class FollowerSerialzier(serializers.ModelSerializer):
    user = UserSerializer(source='from_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model = Friendship
        fields = ('user', 'created_at')

