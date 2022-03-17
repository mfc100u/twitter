from newsfeeds.models import NewsFeed
from friendships.services import FriendshipService

class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
       # 错误的方法
        # 不可以将数据库操作放在 for 循环里面，效率会非常低
        # for follower in FriendshipService.get_followers(tweet.user):
        #     NewsFeed.objects.create(
        #         user=follower,
        #         tweet=tweet,
        #     )

        # 正确的方法：使用 bulk_create，会把 insert 语句合成一条
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.objects.bulk_create(newsfeeds)

        # 这整个API的调用都是在tweet 模块中create api 中调用的

        # 整体的流程是 某人发了一条推特，获取这个用户所有的follower (从FriendshipService模块中)
        # 然后在 NewsFeed 模块中 添加 N 条记录，每个记录就是 每个follower收到消息

