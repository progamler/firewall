from django.db import models

# Create your models here.
class protocol(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class application(models.Model):
    name = models.CharField(max_length=255)
    port = models.IntegerField()
    protocol = models.ForeignKey(protocol)

    def __str__(self):
        return self.name


class zone(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class host(models.Model):
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(zone)
    ip = models.IPAddressField()
    prefix = models.IntegerField()

    def __str__(self):
        return self.name


class firewall(models.Model):
    name = models.CharField(max_length=255)
    ip = models.IPAddressField()

    def __str__(self):
        return self.name


class rule(models.Model):
    name = models.CharField(max_length=255)
    firewall = models.ForeignKey(firewall)
    prio = models.IntegerField()
    permit = models.BooleanField()

    def __str__(self):
        return self.name

class src_address(models.Model):
    rule = models.ForeignKey(rule)
    host = models.ForeignKey(host, related_name='SRC_HOST')


class dst_address(models.Model):
    rule = models.ForeignKey(rule)
    host = models.ForeignKey(host, related_name='DST_HOST')

class rule_app(models.Model):
    rule = models.ForeignKey(rule)
    application = models.ForeignKey(application)



