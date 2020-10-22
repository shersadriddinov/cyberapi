from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('api/', include('v1.urls')),
	path('socket/', include('socket_handler.urls')),
	path('store/', include('store.urls')),
	path('api-token-auth/', obtain_auth_token),
	path('admin/doc/', include('django.contrib.admindocs.urls')),
	path('admin/', admin.site.urls)
]

# When you want switch the localization on, uncomment this and remove similar path lines from original urlpatterns above
# urlpatterns += i18n_patterns(
#     path('admin/doc/', include('django.contrib.admindocs.urls')),
#     path('admin/', admin.site.urls),
# )
