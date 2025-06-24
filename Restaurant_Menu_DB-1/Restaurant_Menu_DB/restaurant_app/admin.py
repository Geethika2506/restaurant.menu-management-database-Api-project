
from django.contrib import admin
from .models import (
    Restaurant, Menu, MenuSection, Menu_MenuSection,
    MenuItem, DietaryRestriction, MenuItem_DietaryRestriction,
    ProcessingLog
)

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuSection)
admin.site.register(Menu_MenuSection)
admin.site.register(MenuItem)
admin.site.register(DietaryRestriction)
admin.site.register(MenuItem_DietaryRestriction)
admin.site.register(ProcessingLog)
