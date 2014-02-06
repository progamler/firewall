from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from core import models
from allauth.account.decorators import verified_email_required
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
        fields = ['name', 'firewall', 'permit']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'firewall': forms.Select(attrs={'class':'form-control'}),
            'permit': forms.CheckboxInput(attrs={'class':'form-control'}, ),
        }
class srcForm(forms.ModelForm):
    class Meta:
        model = models.src_address
        fields = ['host']
        labels = {
            'host': ('Source'),
        }
        widgets = {
            'host': forms.SelectMultiple(attrs={'class':'form-control'}),

        }
class dstForm(forms.ModelForm):
    class Meta:
        model = models.dst_address
        fields = ['host']
        labels = {
            'host': ('Destination'),
        }
        widgets = {
            'host': forms.SelectMultiple(attrs={'class':'form-control'}),

        }
class appForm(forms.ModelForm):
    class Meta:
        model = models.rule_app
        fields = ['application']
        widgets = {
            'application': forms.SelectMultiple(attrs={'class':'form-control'}),

        }
class newappForm(forms.ModelForm):
    class Meta:
        model = models.application
        
class zoneForm(forms.ModelForm):
    class Meta:
        model = models.zone
        
class firewallForm(forms.ModelForm):
    class Meta:
        model = models.firewall

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/?next=%s' % request.path)
    return render(request, "home.html")

@verified_email_required
def display_rule(request, rule_id):
    rule = get_object_or_404(models.rule, pk=rule_id)
    src = get_list_or_404(models.src_address, rule=rule.id)
    dst = get_list_or_404(models.dst_address, rule=rule.id)
    app = get_list_or_404(models.rule_app, rule=rule_id)
    src_zone = src[0].host.zone
    dst_zone = dst[0].host.zone
    return render(request, "juniper.html", {'rule': rule, 'src': src, 'dst': dst, 'application': app, 'src_zone':src_zone, "dst_zone": dst_zone})

@verified_email_required
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

@verified_email_required
def create_app(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = newappForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return redirect('/create/application/') # Redirect after POST
    else:
        form = newappForm() # An unbound form
    return render(request, 'success.html', {
        'form': form,
    })

@verified_email_required
def create_zone(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = zoneForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return redirect('/create/zone/') # Redirect after POST
    else:
        form = zoneForm() # An unbound form
    return render(request, 'success.html', {
        'form': form,
    })

@verified_email_required
def create_firewall(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = firewallForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return redirect('/create/zone/') # Redirect after POST
    else:
        form = firewallForm() # An unbound form
    return render(request, 'success.html', {
        'form': form,
    })
    
@verified_email_required
def save_rule(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        rule = ruleForm(request.POST) # A form bound to the POST data
        src = srcForm(request.POST)
        dst = dstForm(request.POST)
        app = appForm(request.POST)
        firewall= get_object_or_404(models.firewall, pk=request.POST['firewall'])
        s_rule = models.rule(name=request.POST['name'], firewall=firewall,permit=request.POST['permit'],prio=-1)
        s_rule.save()
        for data in request.POST.getlist('src-host'):
            host = get_object_or_404(models.host, pk=data)
            s_src = models.src_address(rule=s_rule, host=host)
            s_src.save()
        for data in request.POST.getlist('dst-host'):
            host = get_object_or_404(models.host, pk=data)
            s_dst = models.dst_address(rule=s_rule, host=host)
            s_dst.save()
        for data in request.POST.getlist('application'):
            app = get_object_or_404(models.application, pk=data)
            s_app = models.rule_app(rule=s_rule, application=app)
            s_app.save()


        return render(request, 'debug.html', {'debug': [request.POST.getlist('dst-host'),request.POST.getlist('src-host'),request.POST.getlist('application'), request.POST] })

    else:
        rule = ruleForm() # An unbound form
        src = srcForm(prefix='src')
        dst = dstForm(prefix='dst')
        app = appForm()
    return render(request, 'create/create_rule.html', {
        'rule': rule, 'src':src, 'dst':dst, 'app':app,
    })


@verified_email_required
def list_rules(request):
    zone = get_list_or_404(models.zone)
    host = get_list_or_404(models.host)
    application = get_list_or_404(models.application)
    firewall = get_list_or_404(models.firewall)
    rule = get_list_or_404(models.rule)
    return render(request, "list_rules.html",
                  {'host': host, 'application': application, 'firewall': firewall, 'rule': rule})

