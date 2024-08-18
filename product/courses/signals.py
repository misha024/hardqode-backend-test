from django.db.models import Count, Value
from django.db.models.functions.text import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Course, Group, UserToGroup
from users.models import CustomUser, Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        [group] = Group.objects.filter(course=instance.course).annotate(
            user_count=Coalesce(Count('users'), Value(0))
        ).order_by('user_count')[:1]

        UserToGroup.objects.create(group=group, user=instance.user)


@receiver(post_save, sender=Course)
def post_save_course(sender, instance: Course, created, **kwargs):
    """
    Создаем 10 групп при создании курса
    """

    if created:
        for i in range(10):
            Group.objects.create(title=f"Group{i}", course=instance)
