from django.contrib import admin
from django.http import Http404

class SubdomainAdmin(admin.ModelAdmin):

    exclude = ('subdomain',)

    def queryset(self,request):
        qs = super(SubdomainAdmin, self).queryset(request)
        return get_queryset(request,qs)
        
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        the_model = db_field.related.parent_model
        
        if hasattr(the_model,'subdomain'):
            kwargs['queryset'] = the_model.objects.filter(subdomain=request.subdomain)
        return super(SubdomainAdmin,self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.subdomain = request.subdomain
        obj.save()
        
def get_queryset(request,qs):
    """
    Filter the objects displayed in the change_list to only
    display those for the currently signed in user.
    """
    #Super user going to asimpleerp.com/admin displays all entries
    if request.mainsite and request.user.is_superuser:
        return qs
    #Super user or subdomain user going to their subdomain shows their entries
    elif request.subdomain and (request.user.is_superuser or request.subdomain.user == request.user):
        return qs.filter(subdomain=request.subdomain)
    else:
        raise Http404
