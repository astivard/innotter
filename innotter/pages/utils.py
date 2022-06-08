from pages.serializers import PageDetailSerializer, AdminPageDetailSerializer, ModerPageDetailSerializer

user_role_serializers_dict = {
    'admin': AdminPageDetailSerializer,
    'moderator': ModerPageDetailSerializer,
    'user': PageDetailSerializer
}
