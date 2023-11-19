from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsEmployer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsNotEmployer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff == False)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.user == request.user
        else:
            return False


# class IsStaff(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.user:
#             if request.user.is_superuser:
#                 return True
#             else:
#                 return False
#         else:
#             return False


# class NotStaff(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.user:
#             if request.user.is_staff:
#                 return False
#             else:
#                 return True
#         else:
#             return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
