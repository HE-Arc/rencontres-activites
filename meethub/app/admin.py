from django.contrib import admin

from .models import Activity, Tag, WaitingUser, Invitation

admin.site.register(Activity)
admin.site.register(Tag)
admin.site.register(WaitingUser)
admin.site.register(Invitation)