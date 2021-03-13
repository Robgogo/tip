
from django import forms
from django.contrib import admin
from api.models.user import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import models as django_models

from api.views.file_handler import ServiceTableViewSet
from api.models.incidents import Department, CriticalService, CriticalIncident, RaisedIncident, ClosedIncident, BacklogIncident


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'role', 'username', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'username')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'first_name', 'last_name', 'username', 'is_staff', 'role', 'is_superuser')
    list_filter = ('id',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username'), }),
        ('Permissions', {'fields': ('is_staff',), }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('-created',)
    filter_horizontal = ()


# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ('department_code', 'department_name', 'department_desc')


class ServiceAdmin(admin.ModelAdmin):
    model = CriticalService
    list_display = ('id', 'service', 'application')


class RaisedIncidentAdmin(admin.ModelAdmin):
    model = RaisedIncident
    list_display = ('id', 'incident_id', 'priority', 'incident_type', 'incident_status', 'created_date', 'resolution_date', 'department')


class ClosedIncidentAdmin(admin.ModelAdmin):
    model = ClosedIncident
    list_display = ('id', 'incident_id', 'priority', 'incident_type', 'incident_status', 'created_date', 'resolution_date', 'department')


class BacklogIncidentAdmin(admin.ModelAdmin):
    model = BacklogIncident
    list_display = ('id', 'incident_id', 'priority', 'incident_type', 'incident_status', 'created_date', 'resolution_date', 'department')


class CriticalIncidentAdmin(admin.ModelAdmin):
    model = CriticalIncident
    list_display = ('id', 'incident_id', 'priority', 'incident_status', 'created_date', 'resolution_date', 'application')


admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(CriticalService, ServiceAdmin)
admin.site.register(RaisedIncident, RaisedIncidentAdmin)
admin.site.register(ClosedIncident, ClosedIncidentAdmin)
admin.site.register(BacklogIncident, BacklogIncidentAdmin)
admin.site.register(CriticalIncident, CriticalIncidentAdmin)

admin.site.unregister(Group)
