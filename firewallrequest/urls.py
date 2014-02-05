from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'core.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^show/rule/(?P<rule_id>\d+)/$', 'core.views.display_rule', name='show_rule'),
                       url(r'^create/host/$', 'core.views.create_host', name='create_host'),
                       url(r'^create/rule/$', 'core.views.create_rule', name='create_rule'),
                       url(r'^save/rule/$', 'core.views.save_rule', name='save_rule'),
                       url(r'^list/rules/$', 'core.views.list_rules', name='list_rules')
)
