'''Defines URL patterns for learning_logs'''

from django.urls import path
from . import views

app_name = 'learning_logs' # helps distinguish this url file from others in the project
urlpatterns = [
    #HOMEPAGE
    path('', views.index, name='index'),
    #Page that shows all topics
    path('topics/', views.topics, name='topics'),
    #Page that shows individual topics
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
    path('delete_entry/<int:entry_id>', views.delete_entry, name='delete_entry'),
    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    path('search_bar', views.search, name='search_logs')
]
