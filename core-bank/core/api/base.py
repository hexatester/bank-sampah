from rest_framework import mixins, status, viewsets, serializers
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response


class BaseUserViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer: serializers.ModelSerializer = self.get_serializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
        else:
            serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def get_queryset(self, *args, **kwargs):
        queryset = super(BaseUserViewSet,
                         self).get_queryset(*args, **kwargs)
        return queryset.filter(
            user=self.request.user,
        )

    def get_object(self, *args, **kwargs):
        if 'pk' in self.request.parser_context['kwargs']:
            obj = get_object_or_404(
                self.get_queryset(),
                pk=self.request.parser_context['kwargs']['pk'],
            )
        else:
            obj = get_object_or_404(
                self.get_queryset(),
            )
        self.check_object_permissions(self.request, obj)
        return obj
