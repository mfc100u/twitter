from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from friendship.models import Friendship
from friendships.api.serializers import (
    FollowingSerializer,
    FollowerSerializer,
    FriendshipSerializerForCreate,
)
from django.contrib.auth.models import User

class FriendshipViewSet(viewsets.GenericViewSet):
    # 我们希望POST /api/friendship/1/follow 是取follow user_id= 1 的用户
    # 因此这里 queryset需要是User.objects.all()
    # 如果是 Friendship.objects.all的话就会出现 404 not found
    # 因为 detail=True 的actions会默认先去调用 get_object()也就是
    # queryset.filet(pk=1) 查询这个object在不在
    queryset = User.objects.all()

    @action(method=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        # GET /api/friendship/1/followers/
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowerSerializer(friendships, many=True)
        return Response(
            {'followers': serializer.data},
            status=status.HTTP_200_OK,
        )
