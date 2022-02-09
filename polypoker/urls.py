from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  path('', include('tables.urls')),
                  path('poker/', include('poker.urls')),
                  path('leaderboard/', include('leaderboard.urls')),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('accounts.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('how-to-play/', include('rules.urls')),
              ] 
