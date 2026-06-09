from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(NamazStatus)
class NamazStatusAdmin(admin.ModelAdmin):
    list_display = ('date', 'fajar_farz', 'zuhar_farz', 'asar', 'maghrib_farz', 'isha_farz', 'percentage', 'growth')
    ordering = ('-date',)
@admin.register(NamazReason)
class NamazReasonAdmin(admin.ModelAdmin):
    list_display = ('status',)
@admin.register(DailyQuranReading)
class QuranDailyReadingAdmin(admin.ModelAdmin):
    list_display = ('date', 'ruku', 'pages', 'points', 'growth')
    ordering = ('-date',)
@admin.register(sleep_track)
class sleep_track_admin(admin.ModelAdmin):
    list_display = ('date','sleep_time','wakeup_time','duration')
    ordering = ('-date',)
@admin.register(college_studies)
class college_studies_admin(admin.ModelAdmin):
    list_display = ('date','start_time','end_time','duration','subject')
    ordering = ('-id',)