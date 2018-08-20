from django.contrib import admin

from task.models import TaskModel


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('status',)
    list_display = ('id', 'create_time', 'start_time', 'exec_time', 'status')
    fieldsets = [
        ('Date information', {'fields': ['create_time', 'start_time', 'exec_time'], 'classes': ['expand']}),
        ('Status', {'fields': ['status'], 'classes': ['expand']})
    ]


admin.site.register(TaskModel, TaskAdmin)
