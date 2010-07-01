# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth import login,authenticate

from subdomain_admin.forms import SubdomainUserForm

def create_subdomain(request):
    form = SubdomainUserForm(request.POST or None)
    if form.is_valid():
        username, password, subdomain = form.save()
        user = authenticate(username=username,password=password)
        login(request,user)
        request.user.message_set.create(message='You have successfully registered %s'%subdomain.get_absolute_url())
        return redirect("%s/"%(subdomain.get_absolute_url()))
    
    return render_to_response('subdomain_admin/createsite.html',
                              {'form':form},
                              RequestContext(request))

