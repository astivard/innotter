from pages.serializers import PageDetailSerializer, AdminPageDetailSerializer, ModerPageDetailSerializer, \
    AdminPageListSerializer, UserPageListSerializer, ModerPageListSerializer

user_role_detail_serializers_dict = {
    'admin': AdminPageDetailSerializer,
    'moderator': ModerPageDetailSerializer,
    'user': PageDetailSerializer
}

user_role_list_serializers_dict = {
    'admin': AdminPageListSerializer,
    'moderator': ModerPageListSerializer,
    'user': UserPageListSerializer
}
