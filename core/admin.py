from django.contrib import admin
from core import models
# Register your models here.
class hostAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'ip', 'prefix')


class ruleAdmin(admin.ModelAdmin):
    list_display = ('name', 'src', 'dst', 'application')


class firewallAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip')


class applicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'protocol', 'port')


admin.site.register(models.protocol)
admin.site.register(models.application, applicationAdmin)
admin.site.register(models.host, hostAdmin)
admin.site.register(models.zone)
admin.site.register(models.rule, ruleAdmin)
admin.site.register(models.firewall, firewallAdmin)

