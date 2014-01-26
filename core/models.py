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
    application = models.ForeignKey(application)
    src = models.ForeignKey(host, related_name='SRC_HOST')
    dst = models.ForeignKey(host, related_name='DST_HOST')
    firewall = models.ForeignKey(firewall)
    permit = models.BooleanField()

    def __str__(self):
        return self.name


