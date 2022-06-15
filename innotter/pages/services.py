from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from pages.models import Page, Tag
from pages.serializers import FollowerSerializer, AddTagSerializer
from users.models import User


def get_unblocked_pages(is_owner_page: bool, owner=None) -> Page:
    pages = Page.objects.filter(Q(is_blocked=False),
                                Q(unblock_date__isnull=True) |
                                Q(unblock_date__lt=timezone.now())).order_by('id')
    if is_owner_page:
        pages = pages.filter(owner=owner)

    return pages


def get_blocked_pages(self) -> Response:
    all_blocked_pages = Page.objects.filter(is_blocked=True).order_by('id')
    if all_blocked_pages:
        serializer = self.get_serializer(all_blocked_pages, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not blocked pages.'})


def get_permissions_list(self, permission_classes_dict: dict) -> list:
    permission_classes = permission_classes_dict.get(self.action, list())
    return [permission() for permission in permission_classes]


def get_page_followers(self, page_pk: int) -> Response:
    all_page_followers = get_object_or_404(Page, pk=page_pk).followers.all().order_by('id')
    if all_page_followers:
        serializer = self.get_serializer(all_page_followers, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not followers on this page.'})


def get_page_follow_requests(self, page_pk: int) -> Response:
    all_page_follow_requests = get_object_or_404(Page, pk=page_pk).follow_requests.all().order_by('id')
    if all_page_follow_requests:
        serializer = self.get_serializer(all_page_follow_requests, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not follow requests on this page.'})


def get_all_follow_requests(self) -> Response:
    pages = Page.objects.filter(owner=self.request.user)
    all_follow_requests = list()
    for page in pages:
        for potential_follower in page.follow_requests.all():
            all_follow_requests.append(potential_follower)
    if all_follow_requests:
        serializer = self.get_serializer(all_follow_requests, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not follow requests.'})


def get_all_follow_requests_queryset(user: User) -> User:
    pages = Page.objects.filter(owner=user)
    all_follow_requests = list()
    for page in pages:
        for potential_follower in page.follow_requests.all():
            all_follow_requests.append(potential_follower)
    return User.objects.filter(username__in=all_follow_requests).order_by('id')


def follow_page(self, page_pk: int) -> Response:
    current_user = self.request.user
    page = get_object_or_404(Page, pk=page_pk)
    if page.is_private:
        if not page.follow_requests.contains(current_user):
            page.follow_requests.add(self.request.user)
            return Response({'detail': f'You have successfully applied for a subscription to {page.name}.'})
        return Response({'detail': f'You have already applied for a subscription to {page.name}.'})
    else:
        if not page.followers.contains(current_user):
            page.followers.add(self.request.user)
            return Response({'detail': f'You have successfully followed {page.name}.'})
        return Response({'detail': f'You are already following {page.name}.'})


def accept_follow_request(request, page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    serializer = FollowerSerializer(data=request.data)
    if serializer.is_valid():
        potential_follower = get_object_or_404(User, email=serializer.validated_data['email'])
        if not page.followers.contains(potential_follower):
            page.followers.add(potential_follower)
            page.follow_requests.remove(potential_follower)
            return Response(
                {'detail': f'You have successfully accepted \'{potential_follower.username}\' to followers.'})
        return Response({'detail': f'User \'{potential_follower.username}\' is already your follower.'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def deny_follow_request(request, page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    serializer = FollowerSerializer(data=request.data)
    if serializer.is_valid():
        potential_follower = get_object_or_404(User, email=serializer.validated_data['email'])
        if page.followers.contains(potential_follower):
            page.follow_requests.remove(potential_follower)
            return Response(
                {'detail': f'You have successfully denied \'{potential_follower.username}\' from follow requests.'})
        return Response({'detail': f'User \'{potential_follower.username}\' is not in follow requests.'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def accept_all_follow_requests(page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all()
    if follow_requests:
        for potential_follower in follow_requests:
            page.followers.add(potential_follower)
            page.follow_requests.remove(potential_follower)
        return Response({'detail': 'You have successfully accepted all follow requests.'})
    return Response({'detail': 'You don\'t have follow requests.'})


def deny_all_follow_requests(page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all()
    if follow_requests:
        for potential_follower in follow_requests:
            page.follow_requests.remove(potential_follower)
        return Response({'detail': 'You have successfully denied all follow requests.'})
    return Response({'detail': 'You don\'t have follow requests.'})


def get_page_tags(self, page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    page_tags = page.tags.all()
    if page_tags:
        serializer = self.get_serializer(page_tags, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'There are not tags on this page.'})


def add_tag_to_page(request, page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    serializer = AddTagSerializer(data=request.data)
    if serializer.is_valid():
        tag = get_object_or_404(Tag, name=serializer.validated_data['name'])
        if not page.tags.contains(tag):
            page.tags.add(tag)
            return Response(
                {'detail': f'You have successfully added tag \'{tag.name}\' to page \'{page.name}\'.'})
        return Response({'detail': f'Tag \'{tag.name}\' is already in {page.name} tags.'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def remove_tag_from_page(request, page_pk: int) -> Response:
    page = get_object_or_404(Page, pk=page_pk)
    serializer = AddTagSerializer(data=request.data)
    if serializer.is_valid():
        tag = get_object_or_404(Tag, name=serializer.validated_data['name'])
        if page.tags.contains(tag):
            page.tags.remove(tag)
            return Response(
                {'detail': f'You have successfully removed tag \'{tag.name}\' from page \'{page.name}\'.'})
        return Response({'detail': f'Tag \'{tag.name}\' is not in {page.name} tags.'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
