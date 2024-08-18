from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import Subscription


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs.get("course_id")
        return request.user.is_staff or Subscription.objects.get(user=request.user, course_id=course_id)

    def has_object_permission(self, request, view, obj):
        course_id = view.kwargs.get("course_id")
        return request.user.is_staff or Subscription.objects.get(user=request.user, course_id=course_id)


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
