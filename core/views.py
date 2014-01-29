from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages

from core import models

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/?next=%s' % request.path)
    return render(request, "home.html")


def display_rule(request, rule_id):
    rule = get_object_or_404(models.rule, pk=rule_id)
    src = get_list_or_404(models.src_address, rule=rule.id)
    dst = get_list_or_404(models.dst_address, rule=rule.id)
    app = get_list_or_404(models.rule_app, rule=rule_id)
    src_zone = src[0].host.zone
    dst_zone = dst[0].host.zone
    return render(request, "juniper.html", {'rule': rule, 'src': src, 'dst': dst, 'application': app, 'src_zone':src_zone, "dst_zone": dst_zone})


def create_host(request):
    zone = get_list_or_404(models.zone)
    return render(request, "create/create_host.html", {'zone': zone})


def save_host(request):
    zone = get_object_or_404(models.zone, pk=request.POST.get('zone'))
    try:
        foo = models.host.objects.get(ip=request.POST.get('IP'), name=request.POST.get('hostname'),
                                      zone=request.POST.get('zone'), prefix=request.POST.get('prefix'))

        messages.add_message(request, messages.INFO, 'Already Exist! Try another')
        zone = get_list_or_404(models.zone)
        return render(request, "create/create_host.html", {'zone': zone})
    except models.host.DoesNotExist:
        pass

    host = models.host(name=request.POST.get('hostname'), ip=request.POST.get('IP'), prefix=request.POST.get('prefix'),
                       zone=zone)
    host.save()
    return render(request, "success.html")


def create_rule(request):
    host = get_list_or_404(models.host)
    application = get_list_or_404(models.application)
    firewall = get_list_or_404(models.firewall)
    return render(request, "create/create_rule.html", {'host': host, 'application': application, 'firewall': firewall})


def save_rule(request):
    src = get_object_or_404(models.host, pk=request.POST.get('src'))
    dst = get_object_or_404(models.host, pk=request.POST.get('dst'))
    application = get_object_or_404(models.application, pk=request.POST.get('app'))
    firewall = get_object_or_404(models.firewall, pk=request.POST.get('firewall'))

    #try:
    #foo = models.rule.objects.get(name=request.POST.get('name'), src=request.POST.get('src'), dst=request.POST.get('dst'), application=request.POST.get('app'), firewall=request.POST.get('firewall'))
    #   messages.add_message(request, messages.INFO, 'Already Exist! Try another')
    #  host = get_list_or_404(models.host)
    # application = get_list_or_404(models.application)
    #firewall = get_list_or_404(models.firewall)
    #return render(request, "create/create_rule.html", {'host': host, 'application': application, 'firewall':firewall})
    #except models.host.DoesNotExist:
    #pass

    rule = models.rule(src=src, name=request.POST.get('name'), dst=dst, application=application, firewall=firewall,
                       permit=0)
    rule.save()
    return render(request, "success.html")


def list_rules(request):
    zone = get_list_or_404(models.zone)
    host = get_list_or_404(models.host)
    application = get_list_or_404(models.application)
    firewall = get_list_or_404(models.firewall)
    rule = get_list_or_404(models.rule)
    return render(request, "list_rules.html",
                  {'host': host, 'application': application, 'firewall': firewall, 'rule': rule})
