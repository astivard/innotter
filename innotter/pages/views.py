from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.permissions import IsAdminRole, IsBlockedUser, IsModerRole

from pages.models import Page, Tag
from pages.serializers import (
    AdminPageDetailSerializer,
    FollowersListSerializer,
    ModerPageDetailSerializer,
    PageDetailSerializer,
    StaffPageListSerializer,
    TagSerializer,
    UserPageDetailSerializer,
    UserPageListSerializer,
    FollowerSerializer,
    AddRemoveTagSerializer,
)
from pages.services import (
    accept_all_follow_requests,
    accept_follow_request,
    add_tag_to_page,
    deny_all_follow_requests,
    deny_follow_request,
    follow_page,
    get_blocked_pages,
    get_page_follow_requests,
    get_page_followers,
    get_page_tags,
    get_permissions_list,
    get_unblocked_pages,
    remove_tag_from_page,
    unfollow_page,
)
from users.services import get_presigned_url
from pages.services import upload_page_image_to_s3


class PagesViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    All pages by all users
    List, retrieve (for all users)
    Update (only for admins and moders)
    Non-blocked pages display only for admins and moders
    """

    action_permission_classes = {
        "list": (
            IsAuthenticated,
            ~IsBlockedUser,
        ),
        "retrieve": (
            IsAuthenticated,
            ~IsBlockedUser,
        ),
        "update": (
            IsAuthenticated,
            IsAdminRole | IsModerRole,
        ),
        "partial_update": (
            IsAuthenticated,
            IsAdminRole | IsModerRole,
        ),
        "blocked": (
            IsAuthenticated,
            IsAdminRole | IsModerRole,
        ),
        "followers": (IsAuthenticated, ~IsBlockedUser),
        "follow": (IsAuthenticated, ~IsBlockedUser),
        "unfollow": (IsAuthenticated, ~IsBlockedUser),
    }

    list_serializer_classes = {
        "admin": StaffPageListSerializer,
        "moderator": StaffPageListSerializer,
        "user": UserPageListSerializer,
    }

    detail_serializer_classes = {
        "admin": AdminPageDetailSerializer,
        "moderator": ModerPageDetailSerializer,
        "user": PageDetailSerializer,
    }

    filter_backends = (SearchFilter,)
    search_fields = (
        "name",
        "uuid",
        "tags__name",
    )

    @action(detail=False, methods=["get"], url_path="blocked")
    def blocked(self, request):
        all_blocked_pages = get_blocked_pages()
        serializer = self.get_serializer(all_blocked_pages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="followers")
    def followers(self, request, pk=None):
        all_page_followers = get_page_followers(page_pk=pk)
        serializer = self.get_serializer(all_page_followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="follow")
    def follow(self, request, pk=None):
        is_private = follow_page(user=self.request.user, page_pk=pk)
        if not is_private:
            return Response(
                {"detail": "You have subscribed to the page or you are already a subscriber."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "You have applied for a subscription."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        unfollow_page(user=self.request.user, page_pk=pk)
        return Response(
            {"detail": "You have unsubscribed from the page or have already unsubscribed."},
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        image_s3_path = serializer.data["image_s3_path"]
        if image_s3_path:
            serialized_data = serializer.data
            serialized_data["image_s3_path"] = get_presigned_url(key=image_s3_path)
            return Response(serialized_data)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.role in ("admin", "moderator"):
            return Page.objects.all().order_by("id")
        return get_unblocked_pages(is_owner_page=False)

    def get_serializer_class(self):
        user_role = self.request.user.role
        if self.action in ("list", "blocked"):
            return self.list_serializer_classes.get(user_role)
        elif self.action == "followers":
            return FollowersListSerializer
        return self.detail_serializer_classes.get(user_role)

    def get_permissions(self):
        return get_permissions_list(self, permission_classes_dict=self.action_permission_classes)


class CurrentUserPagesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    Current user pages
    Retrieve, create, update, delete page
    """

    permission_classes = (
        IsAuthenticated,
        ~IsBlockedUser,
    )

    serializer_classes = {
        "list": UserPageListSerializer,
        "create": UserPageListSerializer,
        "page_follow_requests": FollowersListSerializer,
        "all_follow_requests": FollowersListSerializer,
        "followers": FollowersListSerializer,
        "deny_follow_request": FollowerSerializer,
        "accept_follow_request": FollowerSerializer,
        "tags": TagSerializer,
        "add_tag_to_page": AddRemoveTagSerializer,
        "remove_tag_from_page": AddRemoveTagSerializer,
    }

    @action(detail=True, methods=["get"], url_path="followers")
    def followers(self, request, pk=None):
        all_page_followers = get_page_followers(page_pk=pk)
        serializer = self.get_serializer(all_page_followers, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="follow-requests")
    def page_follow_requests(self, request, pk=None):
        page_follow_requests = get_page_follow_requests(page_pk=pk)
        serializer = self.get_serializer(page_follow_requests, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="accept")
    def accept_follow_request(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        accept_follow_request(follower_email=email, page_pk=pk)
        return Response(
            {"detail": "You have successfully accepted user to followers or user is already your follower."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="deny")
    def deny_follow_request(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        deny_follow_request(follower_email=email, page_pk=pk)
        return Response(
            {"detail": "You have successfully removed user from followers or user is already removed."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="accept-all")
    def accept_all_follow_requests(self, request, pk=None):
        accept_all_follow_requests(page_pk=pk)
        return Response({"detail": "You have successfully accepted all follow requests."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="deny-all")
    def deny_all_follow_requests(self, request, pk=None):
        deny_all_follow_requests(page_pk=pk)
        return Response({"detail": "You have successfully denied all follow requests."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="tags")
    def tags(self, request, pk=None):
        page_tags = get_page_tags(page_pk=pk)
        serializer = self.get_serializer(page_tags, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="add-tag")
    def add_tag_to_page(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_name = serializer.validated_data["name"]
        add_tag_to_page(tag_name=tag_name, page_pk=pk)
        return Response(
            {"detail": "You have successfully added tag to page or it's already added."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["delete"], url_path="remove-tag")
    def remove_tag_from_page(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_name = serializer.validated_data["name"]
        remove_tag_from_page(tag_name=tag_name, page_pk=pk)
        return Response(
            {"detail": "You have successfully removed tag from page or it's already removed."},
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        image_s3_path = serializer.data["image_s3_path"]
        if image_s3_path:
            serialized_data = serializer.data
            serialized_data["image_s3_path"] = get_presigned_url(key=image_s3_path)
            return Response(serialized_data)
        return Response(serializer.data)

    def perform_update(self, serializer):
        image_s3_path = serializer.validated_data["image_s3_path"]
        page_id = serializer.data["id"]
        serializer.validated_data["image_s3_path"] = upload_page_image_to_s3(file_path=image_s3_path, page_id=page_id)

    def get_queryset(self):
        return get_unblocked_pages(is_owner_page=True, owner=self.request.user)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, UserPageDetailSerializer)


class TagsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, ~IsBlockedUser)

    action_permission_classes = {
        "list": (
            IsAuthenticated,
            ~IsBlockedUser,
        ),
        "create": (
            IsAuthenticated,
            ~IsBlockedUser,
        ),
        "destroy": (
            IsAuthenticated,
            ~IsBlockedUser,
            IsAdminRole | IsModerRole,
        ),
    }

    def get_permissions(self):
        return get_permissions_list(self, permission_classes_dict=self.action_permission_classes)
