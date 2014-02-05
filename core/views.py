from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages

from core import models

from django import forms



class hostForm(forms.ModelForm):
    class Meta:
        model = models.host

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'zone': forms.Select(attrs={'class':'form-control'}),
            'ip': forms.TextInput(attrs={'class':'form-control'}),
            'prefix': forms.TextInput(attrs={'class':'form-control'})
        }

class ruleForm(forms.ModelForm):
    class Meta:
        model = models.rule

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'src': forms.SelectMultiple(attrs={'class':'form-control'}),
            'dst': forms.SelectMultiple(attrs={'class':'form-control'}),
            'app': forms.SelectMultiple(attrs={'class':'form-control'}),
            'permit': forms.CheckboxInput(attrs={'class':'form-control'}),
        }
class srcForm(forms.ModelForm):
    class Meta:
        model = models.src_address

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'src': forms.SelectMultiple(attrs={'class':'form-control'}),
            'dst': forms.SelectMultiple(attrs={'class':'form-control'}),
            'rule': forms.HiddenInput(),
            'permit': forms.CheckboxInput(attrs={'class':'form-control'}),
        }
class dstForm(forms.ModelForm):
    class Meta:
        model = models.dst_address
class appForm(forms.ModelForm):
    class Meta:
        model = models.rule_app

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
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = hostForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return redirect('/create/rule/') # Redirect after POST
    else:
        form = hostForm() # An unbound form
    return render(request, 'success.html', {
        'form': form,
    })


def create_rule(request):
    host = get_list_or_404(models.host)
    application = get_list_or_404(models.application)
    firewall = get_list_or_404(models.firewall)
    return render(request, "create/create_rule.html", {'host': host, 'application': application, 'firewall': firewall})


def save_rule(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = hostForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return redirect('/create/rule/') # Redirect after POST
    else:
        rule = ruleForm() # An unbound form
        src = srcForm()
        dst = dstForm()
        app = appForm()
    return render(request, 'create/create_rule.html', {
        'rule': rule, 'src':src, 'dst':dst, 'app':app,
    })



def list_rules(request):
    zone = get_list_or_404(models.zone)
    host = get_list_or_404(models.host)
    application = get_list_or_404(models.application)
    firewall = get_list_or_404(models.firewall)
    rule = get_list_or_404(models.rule)
    return render(request, "list_rules.html",
                  {'host': host, 'application': application, 'firewall': firewall, 'rule': rule})
