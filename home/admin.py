from django.contrib import admin
from djcelery.models import TaskMeta


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)
    list_display = ('task_name', 'status', 'date_done', 'result', 'meta')

    def task_name(self, test):
        return test.task_id  # TODO find task name instead


admin.site.register(TaskMeta, TaskMetaAdmin)
