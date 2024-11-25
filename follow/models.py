from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model
User = get_user_model()


class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'followerList')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followingList')
    following_date = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return f'{self.follower} follows {self.followed}'

    class Meta:
        unique_together = ['followed', 'follower']
        constraints = [
            models.CheckConstraint(
                check=~Q(followed=F('follower')),
                name='prevent_self_follow'
            )
        ]
