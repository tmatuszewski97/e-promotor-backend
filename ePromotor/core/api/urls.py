from django.urls import path, include
import core.api.views as views

urlpatterns = [
    path('', views.index, name='index'),
    # Url for login
    path('login/', views.Login.as_view(), name='login'),

    # Urls for management User with any role (only account owner has got permission to views below)
    path('user/',
         views.UserDetail.as_view(), name='user_detail'),
    path('user/change-password/',
         views.UserChangePassword.as_view(), name='user_change_password'),

    # Urls for management Users with administrator role
    path('administrator/register/',
         views.AdministratorRegister.as_view(), name='administrator_register'),
    path('administrator/', views.AdministratorList.as_view(),
         name='administrator_list'),
    path('administrator/<int:pk>/',
         views.AdministratorDetail.as_view(), name='administrator_detail'),

    # Urls for management Users with dean worker role
    path('dean-worker/register/',
         views.DeanWorkerRegister.as_view(), name='dean_worker_register'),
    path('dean-worker/', views.DeanWorkerList.as_view(),
         name='dean_worker_list'),
    path('dean-worker/<int:pk>/',
         views.DeanWorkerDetail.as_view(), name='dean_worker_detail'),

    # Urls for management Users with promoter role
    path('promoter/bulk-delete/', views.PromoterBulkDelete.as_view(),
         name='promoter_bulk_delete'),
    path('promoter/bulk-register/',
         views.PromoterBulkRegister.as_view(), name='promoter_bulk_register'),
    path('promoter/register/',
         views.PromoterRegister.as_view(), name='promoter_register'),
    path('promoter/', views.PromoterList.as_view(),
         name='promoter_list'),
    path('promoter/<int:pk>/',
         views.PromoterDetail.as_view(), name='promoter_detail'),

    # Urls for management Users with student role
    path('student/bulk-delete/', views.StudentBulkDelete.as_view(),
         name='student_bulk_delete'),
    path('student/bulk-register/',
         views.StudentBulkRegister.as_view(), name='student_bulk_register'),
    path('student/register/',
         views.StudentRegister.as_view(), name='student_register'),
    path('student/', views.StudentList.as_view(),
         name='student_list'),
    path('student/<int:pk>/',
         views.StudentDetail.as_view(), name='student_detail'),

    # Urls for management Files
    path('file/add/', views.FileAdd.as_view(), name='file_add'),
    path('file/', views.FileList.as_view(), name='file_list'),
    path('file/<int:pk>/',
         views.FileDetail.as_view(), name='file_detail'),

    # Urls associated with Records - for dean workers
    path('record/summary/', views.RecordListSummary.as_view(),
         name='record_list_summary'),
    path('record/summary/csv/', views.RecordListSummaryToCsvFile.as_view(),
         name='record_list_summary_csv'),
    path('record/revoke/', views.RevokeRecords.as_view(), name='record_revoke'),

    # Urls associated with Records - for promoters
    path('record/status/', views.GetElectionsStatus.as_view(),
         name='elections_status'),
    path('promoter/record/', views.RecordListForPromoter.as_view(),
         name='record_list_for_promoter'),
    path('promoter/record/<int:pk>/',
         views.RecordDetailForPromoter.as_view(), name='record_detail_for_promoter'),

    # Urls associated with Records - for students
    path('student/record/', views.RecordListForStudent.as_view(),
         name='record_list_for_student'),
    path('student/record/<int:pk>/',
         views.RecordDetailForStudent.as_view(), name="record_detail_for_student"),
    path('student/record/<int:pk>/promoter/',
         views.PromoterListForRecord.as_view(), name='record_promoter_list_for_student'),
    path('student/record/<int:pk>/promoter/<int:pk_2>/',
         views.PromoterDetailForRecord.as_view(), name='record_promoter_detail_for_student'),

]
