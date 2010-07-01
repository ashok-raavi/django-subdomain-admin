from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms
from subdomains.models import Subdomain

class SubdomainUserForm(UserCreationForm):
    subdomain_title = forms.CharField(max_length=50,label='Site name')
    
    def clean(self):
        subdomain_value = self.cleaned_data['username']
        if subdomain_value=='www':
            raise forms.ValidationError('This subdomain cannot be registered')
        try:
            Subdomain.objects.get(subdomain_text=subdomain_value)
        except Subdomain.DoesNotExist:
            return self.cleaned_data
        raise forms.ValidationError('This subdomain cannot be registered')
    
    def save(self,**kwargs):
        user = super(SubdomainUserForm,self).save(**kwargs)
        user.is_staff=True
        group = Group.objects.get(name='SubUser')
        user.groups.add(group)
        user.save()
        cd = self.cleaned_data
        username, password = cd['username'], cd['password2']
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = cd['username'],
                                                             name = cd['subdomain_title'],
                                                             description = "Descriptions",
                                                             user = user)
        subdomain.save()
        # auto_create_menus(subdomain,user)
        return username, password, subdomain
    
#    
#def autopopulate_data():
#    from simplecms.cms.models import Menu, Article, Category
#    menus = Menu.objects.filter(subdomain=None)
#    for el in menus:
#        Menu.objects.create(subdomain=subdomain,name=el.name)
#    try:
#        cats = Category.objects.filter(subdomain=None)
#        for cat in cats:
#            Category.objects.create(title=cat.title,menu=Menu.objects.get(name))
#        
#        articles = Article.objects.filter(subdomain=None)
#        for ar in articles:
#            pass
#    except:
#        pass
#
#    
#def auto_create_menus(subdomain,user):
#    from simplecms.cms.models import Menu, Article, Category
#    menus = Menu.objects.filter(subdomain=None)
#    menu_objects = []
#    for el in menus:
#        menu_objects.append(Menu.objects.create(subdomain=subdomain,name=el.name))
#    scat = Category(menu=menu_objects[0], title='Sample Category', subdomain=subdomain,
#                    slug='sample-category',path='sample',short_title='Sample')
#    scat.save()
#    from django.contrib.auth.models import User
#    a = Article(author=user, path='home', slug='main', subdomain=subdomain, text='This is an empty sample article. Please edit or change this in the erp',
#                title='Home Page',category=scat)
#    a.save()
#    