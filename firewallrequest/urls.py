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
                       url(r'^create/app/$', 'core.views.create_app', name='create_app'),
                       url(r'^create/zone/$', 'core.views.create_zone', name='create_zone'),
                       url(r'^create/firewall/$', 'core.views.create_firewall', name='create_firewall'),
                       url(r'^save/rule/$', 'core.views.save_rule', name='save_rule'),
                       url(r'^list/rules/$', 'core.views.list_rules', name='list_rules')
)
