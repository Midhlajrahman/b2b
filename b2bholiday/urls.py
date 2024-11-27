from django.conf import settings
from django.contrib import admin
from django.urls import include,path
from django.conf.urls.static import static

urlpatterns = (
        [
        path("admin/", admin.site.urls),
        path("", include("web.urls", namespace="web")),
        path("ticket/",include("ticket.urls",namespace="ticket")),
        path("core/",include("core.urls",namespace="core")),
        path('accounts/', include('registration.backends.default.urls')),
        path('accounts/', include('registration.backends.simple.urls')),
        
        path('tinymce/', include('tinymce.urls')),

    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)


admin.site.site_header = "B2B Holidays Administration"
admin.site.site_title = "B2B Holidays  Admin Portal"
admin.site.index_title = "Welcome to B2B Holidays  Admin Portal"