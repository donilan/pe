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
    url(r'^$', 'apps.views.upload'),
    url(r'^upload', 'apps.views.upload'),
    url(r'^parse', 'apps.views.parse'),
    url(r'^load/(?P<offset>\d+)/(?P<_length>\d+)', 'apps.views.load'),
)
