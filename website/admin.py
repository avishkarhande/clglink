from django.contrib import admin
from website.models import Profile,Skills,Education,work,achievement,Notification
# Register your models here.
admin.site.register(Profile)
admin.site.register(Skills)
admin.site.register(Education)
admin.site.register(work)
admin.site.register(achievement)
admin.site.register(Notification)