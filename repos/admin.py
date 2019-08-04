from django.contrib import admin

# Register your models here.
from repos import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Asset)
admin.site.register(models.Department)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC)
admin.site.register(models.Server)
admin.site.register(models.UserGroup)
admin.site.register(models.AdminGroup)
admin.site.register(models.AG)
admin.site.register(models.UG)