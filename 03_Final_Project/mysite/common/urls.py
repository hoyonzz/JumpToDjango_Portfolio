from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy


app_name = 'common'


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # 비밀번호 초기화 요청 폼
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='common/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url=reverse_lazy('common:password_reset_done')
        ), name='password_reset'),

    # 비밀번호 이메일 전송 완료 안내
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='common/password_reset_done.html'),
        name='password_reset_done'),

    # 이메일 링크 클릭 후 비밀번호 재설정 폼(uidb64, token 포함)
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='common/password_reset_confirm.html',
            success_url=reverse_lazy('common:password_reset_complete')
        ), name='password_reset_confirm'),

    # 비밀번호 재설정 완료 안내
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='common/password_reset_complete.html'),
        name='password_reset_complete'),
    
    # 로그인한 사용자가 비밀번호 변경
    path('password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='common/password_change_form.html',
            success_url=reverse_lazy('common:password_change_done')
        ), name='password_change'),

    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='common/password_change_done.html'),
        name='password_change_done'),

    # 프로필 관련
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
