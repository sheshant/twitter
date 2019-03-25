from rest_framework.permissions import IsAuthenticated


class TokenPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            return True
        return False
