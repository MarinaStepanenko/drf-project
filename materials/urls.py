from tkinter.font import names

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from materials.views import (CourseViewSet, LessonCreateApiView,
                             LessonDestroyApiView, LessonListApiView,
                             LessonRetrieveApiView, LessonUpdateApiView)

app_name = "materials"

router = SimpleRouter()
router.register(r"courses", CourseViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
]
