from django.db import models


class Page(models.Model):
    """User page"""

    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('pages.Tag', related_name='pages')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User', related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag"""

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
