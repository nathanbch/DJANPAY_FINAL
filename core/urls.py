from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transfer/', views.transfer_view, name='transfer'),

    path('mentions-legales/', TemplateView.as_view(template_name="legal/mentions_legales.html"), name='mentions_legales'),
    path('politique-confidentialite/', TemplateView.as_view(template_name="legal/politique_confidentialite.html"), name='politique_confidentialite'),
    path('conditions-generales/', TemplateView.as_view(template_name="legal/conditions_generales.html"), name='conditions_generales'),

    path('supprimer-compte/', views.delete_account, name='delete_account'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('create-user/', views.create_user_view, name='create_user'),
    path('account/', views.account_view, name='account'),
    path('history/', views.history_view, name='history'),
    path('profile/', views.profile_view, name='profile'),

]
