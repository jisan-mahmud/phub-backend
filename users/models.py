from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class Follow(models.Model):
    followed = models.ForeignKey(User, models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following_date = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return f'{self.follower} following {self.followed}'
    
    class Meta:
        unique_together= ['followed', 'follower']
        
        constraints = [
            models.CheckConstraint(
                check= ~Q(followed = models.F('follower')),
                name='prevent_self_follow'
            )
        ]
