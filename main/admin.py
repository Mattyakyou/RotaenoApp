from django.contrib import admin
from .models import Diff
from .models import Score





# Register your models here.
admin.site.register(Diff)
admin.site.register(Score)

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)



#name: Mattyakyoukyouso
#email: mattyakyou@gmail.com
#Password: G7#pL9x!vT@3bQz$M2dW