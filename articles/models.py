from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.
class Article(models.Model):
    article_id=models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created_at=models.DateField(auto_now_add=True)
    created_by=models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,blank=True, null=True,related_name='%(class)s_trip_creator_created')
    content=models.TextField(editable=True,blank=False,null=False)
    title = models.CharField(max_length=256)    
    nor_score = models.DecimalField(default=0, decimal_places=4, max_digits=5)
    clicks = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    score_ignore = models.BooleanField(default=False)

    def __str__(self) -> str:
            return self.content[:50]