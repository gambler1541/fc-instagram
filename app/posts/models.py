import re

from django.conf import settings
from django.db import models


class Post(models.Model):
    PATTERN_HASHTAG = re.compile(r'#(\w+)')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('HashTag', blank=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        # 1. related_name은 반대쪽(target)에서 이쪽(source)로의 연결을 만들어주는 Manager
        # 2.  자신이 like_users에 포함이 되는 Post QuerySet Manager
        # 3.  -> 내가 좋아요 누른 Post목록
        related_name='like_posts',
    )

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for tag_name in re.findall(self.PATTERN_HASHTAG, self.content):
            tag, tag_created = HashTag.objects.get_or_create(name=tag_name)
            self.tags.add(tag)

    @property
    def content_html(self):
        return re.sub(
            r'#(?P<tag>\w+)',
            '<a href="/posts/tags/\g<tag>">#\g<tag></a>',
            self.content,
        )


class HashTag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'HashTag (self.name)'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments',
    )
    _author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    _content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment (post: {self.post.pk}, author: {self.author.username})'

    @property
    def author(self):
        if self.is_deleted:
            return None
        return self._author

    @property
    def content(self):
        if self.is_deleted:
            return '삭제된 댓글입니다'
        return self._content

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
