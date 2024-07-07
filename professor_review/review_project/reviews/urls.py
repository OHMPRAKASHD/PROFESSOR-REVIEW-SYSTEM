# reviews/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('add_review/<int:teacher_id>/', views.AddReviewView.as_view(), name='add_review'),
    path('teachers/<int:teacher_id>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('edit_review/<int:teacher_id>/<int:review_id>/', views.EditReviewView.as_view(), name='edit_review'),
    path('delete_review/<int:teacher_id>/<int:review_id>/', views.DeleteReviewView.as_view(), name='delete_review'),
    # Add these URLs for discussions
    path('discussions/', views.DiscussionListView.as_view(), name='discussion_list'),
    path('discussions/<int:discussion_id>/', views.DiscussionDetailView.as_view(), name='discussion_detail'),
    path('add_discussion/', views.add_discussion, name='add_discussion'),
    path('edit_discussion/<int:discussion_id>/', views.edit_discussion, name='edit_discussion'),
    path('edit_reply/<int:discussion_id>/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('delete_reply/<int:discussion_id>/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('delete_discussion/<int:discussion_id>/', views.delete_discussion, name='delete_discussion'),
]
