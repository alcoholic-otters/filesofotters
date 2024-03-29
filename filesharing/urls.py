from django.urls import path

from . import views

app_name = 'filesharing'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('delete/<int:metadata_id>', views.FileDeleteView.as_view(), name='delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('group/manage/', views.ManageGroupsView.as_view(), name='manage-groups'),
    path('group/create/', views.GroupCreateView.as_view(), name='group-create'),
    path('group/delete/<int:id>/', views.GroupDeleteView.as_view(), name='group-delete'),
    path('group/member/add/', views.GroupMemberAddView.as_view(), name='group-member-add'),
    path('group/member/remove/<int:id>/<str:username>/',
        views.GroupMemberRemoveView.as_view(), name='group-member-remove'),
    path('file/groups/set/<int:id>', views.FileGroupsSetView.as_view(), name='file-groups-set'),
    path('tag/create/', views.TagCreateView.as_view(), name='tag-create'),
    path('tag/delete/<int:id>/', views.TagDeleteView.as_view(), name='tag-delete'),
    path('tag/attach/<int:file_id>/', views.TagAttachView.as_view(), name='tag-attach'),
    path('tag/detach/<int:file_id>/<int:tag_id>/',
        views.TagDetachView.as_view(), name='tag-detach'),
    path('search/', views.FileSearchView.as_view(), name='search'),
    path('detail/file/<int:id>/', views.DetailFileView.as_view(), name='detail-file'),
]
