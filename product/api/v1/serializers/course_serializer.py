from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription

from django.db.models import Count, Value
from django.db.models.functions.text import Coalesce



User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    course = serializers.StringRelatedField(read_only=True)
    users = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Group
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_lessons_count(obj: Course = None):
        """Количество уроков в курсе."""
        return Lesson.objects.filter(course=obj).count()

    @staticmethod
    def get_students_count(_self, obj=None):
        """Общее количество студентов на курсе."""
        return Subscription.objects.filter(course=obj).count()

    @staticmethod
    def get_groups_filled_percent(_self, obj: Course = None):
        """Процент заполнения групп, если в группе максимум 30 чел."""
        groups = Group.objects.filter(course=obj).annotate(
            user_count=Coalesce(Count('users'), Value(0))
        )

        percentages = [q.user_count / 30 * 100 for q in groups]

        if not percentages:
            return 0
        return sum(percentages) / len(percentages)

    @staticmethod
    def get_demand_course_percent(_self, obj=None):
        """Процент приобретения курса."""
        return Subscription.objects.filter(course=obj).count() / User.objects.count() * 100

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'cost',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'
