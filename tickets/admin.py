# -*- coding: utf-8 -*-
from django.contrib import admin
from tickets.models import Student, Ticket


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 0


class StudentAdmin(admin.ModelAdmin):

    def admin_ticket_display(self, obj):
        return obj.ticket_or_none is not None
    admin_ticket_display.boolean = True
    admin_ticket_display.short_description = 'karta'
    admin_ticket_display.admin_order_field = 'student__ticket__number'

    list_display = ('code', 'last_name', 'first_name', 'email', 'admin_ticket_display')
    search_fields = ('code', 'last_name', 'first_name', 'email', 'ticket__number')

    inlines = (TicketInline,)

admin.site.register(Student, StudentAdmin)


class TicketAdmin(admin.ModelAdmin):
    def admin_student_display(self, obj):
        return unicode(obj.student)
    admin_student_display.short_description = 'brucoš'
    admin_student_display.admin_order_field = 'student__code'

    list_display = ('number', 'admin_student_display', 'creation_time')
    search_fields = ('number', 'student__last_name', 'student__first_name', 'student__code',  'student__email')

    list_filter = ('creation_time',)
    date_hierarchy = 'creation_time'

admin.site.register(Ticket, TicketAdmin)
