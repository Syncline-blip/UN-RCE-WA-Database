from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Report, Account, Expression_of_interest


admin.site.register(Report)
admin.site.register(Expression_of_interest)

'''
    Django reccomends to inherit from StackedInLine for 
    specific fields
'''
class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False # Avoid deleting accounts if user is not deleted, it must be associated with User, do not delete account without user
    verbose_name_plural = 'Accounts'

'''
    Inherits UserAdmin, responsible for visualising in user admin panel
'''
class CustomisedUserAdmin (UserAdmin):
    inlines = (AccountInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomisedUserAdmin)
admin.site.register(Account)