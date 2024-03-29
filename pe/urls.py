from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pe.views.home', name='home'),
    # url(r'^pe/', include('pe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^exe', 'apps.views.exe'),
    url(r'^dll', 'apps.views.dll'),
    url(r'^$', 'apps.views.upload'),
    url(r'^upload', 'apps.views.upload'),
    url(r'^1.0/parse', 'apps.views.parse01'),
    url(r'^2.0/parse', 'apps.views.parse02'),
)
