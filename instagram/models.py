from django.db import models

from core.models import TimeStampModel

class Post(TimeStampModel):
    message = models.TextField()
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y/%m/%d')
    is_public = models.BooleanField(default=False, verbose_name='공개여부')

    def __str__(self):
        # return f'Custom Post Object ({self.id})'
        return self.message

    def message_length(self):
        return len(self.message)
    message_length.short_description = "메시지 글자수"
