from django.contrib import admin

from blogango.models import Blog, BlogEntry, Comment, BlogRoll

from subdomain_admin.admin import SubdomainAdmin

class BlogEntryAdmin(SubdomainAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
class BlogRollAdmin(SubdomainAdmin):
    pass

admin.site.register(Blog)
admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Comment)
admin.site.register(BlogRoll, BlogRollAdmin)
