from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("Username already exists")


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    ordering = ("username",)
    list_display = ("username",  "first_name", "agent_code",  "is_active", "date_joined", "is_staff", "is_superuser", )
    list_display_links = ("username",)
    readonly_fields = ("last_login", "date_joined", "pk")
    search_fields = ["username",]
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined", "last_login","agent_code")
    fieldsets = (
        ("Basic Info", {"fields": ("username", "password", "email", "agent_code" )}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Groups", {"fields": ("groups",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, MyUserAdmin)