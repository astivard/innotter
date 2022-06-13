from django.utils import timezone
from rest_framework.response import Response

from pages.models import Page
from django.db.models import Q
from typing import Union


def get_unblocked_pages(is_owner_page: bool, owner=None) -> Page:
    if is_owner_page and owner is None:
        raise Exception('The owner must be specified.')

    if is_owner_page:
        pages = Page.objects.filter(Q(owner=owner),
                                    Q(is_blocked=False),
                                    Q(unblock_date__isnull=True) |
                                    Q(unblock_date__lt=timezone.now())).order_by('id')
    else:
        pages = Page.objects.filter(Q(is_blocked=False),
                                    Q(unblock_date__isnull=True) |
                                    Q(unblock_date__lt=timezone.now())).order_by('id')
    return pages


def get_blocked_pages(self) -> Union[Response, dict]:
    all_blocked_pages = Page.objects.filter(is_blocked=True)
    if all_blocked_pages:
        serializer = self.get_serializer(all_blocked_pages, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not blocked pages.'})


def get_permissions_list(self, permission_classes_dict: dict) -> list:
    permission_classes = permission_classes_dict.get(self.action, list())
    return [permission() for permission in permission_classes]


def get_page_followers(self, page_pk: int) -> Response:
    all_page_followers = Page.objects.get(pk=page_pk).followers.all()
    if all_page_followers:
        serializer = self.get_serializer(all_page_followers, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not followers on this page.'})


def get_page_follow_requests(self, page_pk: int) -> Response:
    all_page_follow_requests = Page.objects.get(pk=page_pk).follow_requests.all()
    if all_page_follow_requests:
        serializer = self.get_serializer(all_page_follow_requests, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not follow requests on this page.'})


def follow_page(self, page_pk: int) -> Response:
    current_user = self.request.user
    page = Page.objects.get(pk=page_pk)
    if page.is_private:
        if not page.follow_requests.contains(current_user):
            page.follow_requests.add(self.request.user)
            return Response({'detail': 'You have successfully applied for the following.'})
        return Response({'detail': 'You have already applied for the following.'})
    else:
        if not page.followers.contains(current_user):
            page.followers.add(self.request.user)
            return Response({'detail': 'You have successfully followed page.'})
        return Response({'detail': 'You are already following this page.'})
