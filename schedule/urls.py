from django.urls import path

from . import views

app_name = "schedule"
urlpatterns = [
    # /schedule/
    path('', views.index, name='index'),
    # /schedule/full/<group_number>
    # path('full/<int:group_number>/', views.full_schedule, name='full_schedule'),
    path('full/<int:group_number>/', views.FullScheduleView.as_view(), name='full_schedule'),
    # /schedule/week/<group_number>
    path('week/<int:group_number>/', views.schedule_for_a_week, name='schedule_for_a_week'),
    # /schedule/next_week/<group_number>
    path('next_week/<int:group_number>/', views.ScheduleForNextWeek.as_view(), name='schedule_for_next_week'),
    # /schedule/<group_number> Have to catch a date[!]
    path('<str:target_date>/<int:group_number>/', views.schedule_for_a_day, name='schedule_for_a_day'),
    # /schedule/simple_text/<type>
    path('simple_text/<int:group_number>/<str:type>/', views.simple_text, name='simple_text'),
]
