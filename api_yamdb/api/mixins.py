from api.permissions import IsAdminOrReadOnly
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from .pagination import PagePagination


class MyCustomBaseViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PagePagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
