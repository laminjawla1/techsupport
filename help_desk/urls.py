from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts import views as account_views
from ticket.views import BookTicketView, TicketView, UpdateTicketView, DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls"), name='blog'),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path("password_reset/", 
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path("password_reset_complete/", 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    path("password_reset_confirm/<uidb64>/<token>", 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset/done", 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("password_reset/done", 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("account/", account_views.account, name="account"),
    path("set_language/", account_views.set_language, name="set_language"),
    path('ticket/new', BookTicketView.as_view(), name='book_ticket'),
    path('tickets/<str:username>/tickets', TicketView.as_view(), name='my_tickets'),
    path('tickets/<int:pk>/update', UpdateTicketView.as_view(), name="update_ticket"),
    path('dashboard', DashboardView.as_view(), name="dashboard")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)