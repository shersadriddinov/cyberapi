from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('v1.urls')),
    path('api-token-auth/', obtain_auth_token)
]

urlpatterns += i18n_patterns(
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
)
