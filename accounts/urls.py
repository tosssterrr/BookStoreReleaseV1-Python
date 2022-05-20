from django.urls import path, include, reverse_lazy

from django.contrib.auth import views as auth_views
from accounts.views import show_current_order, show_orders, personal_area, user_login, user_logout, \
    password_reset_request, ActivateUser, register, order_delete_done
from .forms import UserSetPasswordForm, UserPasswordChangeForm


urlpatterns = [
    path('activate/<uid>/<token>/', ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password/password_change.html',
        form_class=UserPasswordChangeForm,
        success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(
        template_name='password/password_change_done.html',
    ), name='password_change_done'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password/password_reset_confirm.html",
        success_url=reverse_lazy('accounts:password_reset_complete'),
        form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/orders/', show_current_order, name='current_order'),
    path('profile/orders', show_orders, name='orders'),
    path('profile/order_delete_done', order_delete_done, name='order_delete_done'),
    path('profile/', personal_area, name='personal_area'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
