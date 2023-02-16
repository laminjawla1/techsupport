from django.contrib import admin
from .models import Ticket, Expert, Branches, Zones
from django.http import HttpResponse
import csv


def export_tickets(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Branch', 'Zone', 'Phone', 'Issue',
                    'Category', 'Status', 'Date Submitted'])
    tickets = queryset.values_list(
        'submitter', 'branch','zone', 'phone', 'issue',
        'category', 'status', 'date_submitted')
    for ticket in tickets:
        writer.writerow(ticket)
    return response


export_tickets.short_description = 'Export as csv'


class PageAdmin(admin.ModelAdmin):
    list_display = ('submitter', 'branch', 'phone', 'issue',
                    'category', 'status', 'date_submitted')
    ordering = ('submitter', 'branch', 'phone', 'issue',
                'category', 'status', 'date_submitted')
    search_fields = ('submitter', 'branch', 'phone', 'issue',
                     'category', 'status', 'date_submitted')
    list_filter = ['submitter', 'branch', 'issue',
                   'category', 'status', 'assigned_to']

    fieldsets = (
        ('Meta Information', {
            'classes': ('collapse',),
            'fields': ('submitter', 'issue', 'description')
        }),
        ('Contact Information', {
            'classes': ('collapse',),
            'fields': ('phone', 'anydesk', 'zone', 'branch')
        }),
        ('Ticket Information', {
            'classes': ('collapse',),
            'fields': ('category', 'status', 'image', 'date_submitted', 'date_closed', 'documentation')
        }),
        ('Ticket Admin', {
            'classes': ('collapse',),
            'fields': ('assigned_to', 'verification')
        }),
    )
    actions = [export_tickets]


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ['name']
    sortable_by = ['name']

class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ['name']
    sortable_by = ['name']


admin.site.register(Ticket, PageAdmin)
admin.site.register(Expert)
admin.site.register(Zones, ZoneAdmin)
admin.site.register(Branches, BranchAdmin)