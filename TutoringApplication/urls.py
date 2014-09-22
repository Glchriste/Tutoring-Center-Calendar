#from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from TutoringApplication.views import *
from django.conf.urls import *
#from django.conf.urls import patterns, include, url
from TutoringApplication import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # (r'^$', main_page),
    (r'^$', RedirectView.as_view(url='portal/')),
    #Admin
    (r'^admin/', include(admin.site.urls)),

    # Register
    (r'^register/$', registration),

    # Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^calendar/', include('django_bootstrap_calendar.urls')),
    #(r'^files/$', file_page),

    # Web portal.
    (r'^portal/', include('portal.urls', namespace="portal")),
    
    #(r'^$', 'portal.views.portal_main_page', name='portal_main_page'),
    #(r'^portal/$', include('portal.urls', namespace="portal", app_name="portal")),
    # Serve static content.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),

    

)