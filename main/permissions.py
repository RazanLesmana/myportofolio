from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(IsPortfolioOwnerOrReadOnly):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or (
            request.user.is_authenticated
            and request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
