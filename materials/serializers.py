from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons_in_course = SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ["name", "description", "count_lessons_in_course", "lessons"]
