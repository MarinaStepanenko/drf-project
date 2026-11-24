from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video_url")]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons_in_course = SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(user=request.user, course=obj).exists()

    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "count_lessons_in_course",
            "lessons",
            "is_subscribed",
        ]


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(user=request.user, course=obj).exists()
