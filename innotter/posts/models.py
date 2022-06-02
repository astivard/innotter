from django.db import models


class Post(models.Model):
    """Post on the page"""

    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page
