from django.db import models


class Page(models.Model):
    """User page"""

    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField("pages.Tag", related_name="pages")

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="pages")
    followers = models.ManyToManyField("users.User", related_name="follows")

    image_s3_path = models.CharField(max_length=200, null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField("users.User", related_name="requests")

    unblock_date = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag"""

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
