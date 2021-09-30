from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_superuser)


# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return (request.user
#                 and request.user.is_authenticated
#                 and request.user.is_active
#                 and request.user.is_admin)


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in ['PUT', 'DELETE']:
            return True
        return obj.author == request.user


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
