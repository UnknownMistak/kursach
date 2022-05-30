from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *
from import_export.admin import ExportActionMixin

class EventAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'place', 'ev_date')

class HistoryExportAdmin(SimpleHistoryAdmin, EventAdmin):
    pass

admin.site.register(Event, HistoryExportAdmin)
admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(Student, SimpleHistoryAdmin)

# Register your models here.
