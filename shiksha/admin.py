from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from shiksha.models import User,CollegeUser,College,Course,Admission
from shiksha.forms import UserAdminCreationForm,UserAdminChangeForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form=UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display =("email","is_superuser")
    list_filter =("email",)
    fieldsets =(
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':()}),
        ('Permissions',{'fields':("is_superuser",)}),
    )
    add_fieldsets =(
        (None,{'classes':('wide',),
        'fields':("email","password1","password2")}
    ),
    )
    search_fields = ("email",)
    ordering=("email",)
    filter_horizontal =()

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
admin.site.register(CollegeUser)
admin.site.register(College)
admin.site.register(Course)
admin.site.register(Admission)