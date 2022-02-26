from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/',views.userProfile,name='profile'),
    path('create-challenge/', views.createChallenge,name='createChallenge'),
    path('create-response/<int:pk>/',views.createResponse,name='createResponse'),


    # urls for password resetting
    path('reset_password/', views.password_reset_request, name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'), 
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password/complete/',PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),name='password_reset_complete'),


    path('my-responses/',views.myResponses,name='myResponses')

]

# For handling photos in DEBUG 
# https://www.geeksforgeeks.org/python-uploading-images-in-django/ 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)