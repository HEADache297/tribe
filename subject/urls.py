from django.urls import path
from . import views

# This code snippet is defining URL patterns for a Django application. Each `path` function call
# specifies a URL pattern along with the corresponding view function that should be called when that
# URL is accessed. Here's a breakdown of each line:
urlpatterns = [
    path('course/<int:id>/', views.course, name='course'),
    path('course/search/<int:subject_id>', views.students_search, name='students_search'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/connect/<int:subject_id>', views.course_url, name='connect_course'),
    path('course/<int:subject_id>/student/<int:student_id>/delete', views.delete_student, name='delete_student'),
    path('course/<int:subject_id>/material/<int:material_id>/delete', views.delete_material, name='delete_material'),
    path('course/<int:subject_id>/material/<int:material_id>', views.material_page, name='material_page'),
    path('course/<int:subject_id>/schedule/<int:schedule_id>/delete', views.delete_schedule, name='delete_schedule'),
    path('course/<int:subject_id>/student/<int:student_id>/add', views.add_student, name='add_student'),
]