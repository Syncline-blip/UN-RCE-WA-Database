from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Report, Account, Expression_of_interest, ReportImages, ReportFiles, Organization


admin.site.register(Expression_of_interest)

'''
    Django reccomends to inherit from StackedInLine for 
    specific fields
'''
class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False # Avoid deleting accounts if user is not deleted, it must be associated with User, do not delete account without user
    verbose_name_plural = 'Accounts'

class ReportImagesInline(admin.TabularInline):
    model = ReportImages
    extra = 1

class ReportFilesInline(admin.TabularInline):
    model = ReportFiles
    extra = 1

class OrganizationInline(admin.TabularInline):
    model = Organization
    extra = 1

'''
    Inherits UserAdmin, responsible for visualising in user admin panel
'''
class CustomisedUserAdmin (UserAdmin):
    inlines = (AccountInLine, )

class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportImagesInline, ReportFilesInline, OrganizationInline]

admin.site.unregister(User)
admin.site.register(User, CustomisedUserAdmin)
admin.site.register(Account)
admin.site.register(Report, ReportAdmin)