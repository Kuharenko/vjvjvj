from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(TaskCategory)
# admin.site.register(Tasks)
admin.site.register(Quests)
admin.site.register(TaskCheckIn)
admin.site.register(TaskUploadImage)
admin.site.register(TaskChoiceRightVariant)
admin.site.register(ResultForUserCheckinTask)
admin.site.register(ResultForUserChoicesTask)
admin.site.register(ResultForUserImageTask)
admin.site.register(ResultQuestByUser)

