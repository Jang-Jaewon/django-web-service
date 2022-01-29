from django.conf import settings
from django.db   import models
from django.urls import reverse
from django.core.validators import MinLengthValidator

from core.models import TimeStampModel


class Post(TimeStampModel):
    author    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message   = models.TextField(validators=[MinLengthValidator(10)])
    photo     = models.ImageField(blank=True, upload_to='instagram/post/%Y/%m/%d')
    tag_set   = models.ManyToManyField('Tag', blank=True)
    is_public = models.BooleanField(default=False, verbose_name='공개여부')

    def __str__(self):
        # return f'Custom Post Object ({self.id})'
        return self.message

    def message_length(self):
        return len(self.message)
    message_length.short_description = "메시지 글자수"

    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])

    class Meta:
        ordering = ['-id']


class Comment(TimeStampModel):
    post        = models.ForeignKey('Post', on_delete=models.CASCADE, limit_choices_to={'is_public':True})
    description = models.TextField()


class Tag(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
