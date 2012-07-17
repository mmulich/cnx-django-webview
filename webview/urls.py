from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'moduleviewer.views.index', name='index'),
    url(r'^content/(?P<id>m\d+)/?$', 'moduleviewer.views.module'),
    url(r'^content/(?P<id>m\d+)@(?P<version>[\d.]+)',
        'moduleviewer.views.module'),
    # Examples:
    # url(r'^$', 'webview.views.home', name='home'),
    # url(r'^webview/', include('webview.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
