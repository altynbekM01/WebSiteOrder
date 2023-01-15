from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from webSite.views import *

urlpatterns = [
    path('', home, name='home'),
    path('api/v1/edit_profile/', edit, name='edit'),
    path('api/v1/profile/<int:pk>/', GetProfile),

    path('api/v1/order/', OrderAPIList.as_view()),
    path('api/v1/order/<int:pk>/', OrderAPIUpdate.as_view()),
    # path('api/v1/orderupdatebyadmin/<int:pk>/', OrderAPIUpdate2.as_view()),
    path('api/v1/orderdelete/<int:pk>/', OrderAPIDestroy.as_view()),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new

]