from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    """Stores restaurant information"""
    name = models.CharField(max_length=255, null=False, default='Unnamed Restaurant')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Menu(models.Model):
    """Represents a menu type for a restaurant. This is the parent object that groups all versions of a menu."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, default='Unnamed Menu')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['restaurant', 'name']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

class MenuVersion(models.Model):
    """Tracks different versions of a menu. Each version contains its own sections and items."""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_index=True)
    version_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255, default='System')
    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text="Indicates if this is the currently active version")

    class Meta:
        unique_together = ['menu', 'version_number']
        ordering = ['-version_number']
        indexes = [
            models.Index(fields=['menu']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.menu.name} v{self.version_number}"

    def save(self, *args, **kwargs):
        """Override save to ensure only one version is active at a time"""
        if self.is_active:
            # Set all other versions of this menu to inactive
            MenuVersion.objects.filter(menu=self.menu).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

class MenuSection(models.Model):
    """Defines sections in a menu version. Now connected to MenuVersion instead of Menu."""
    menu_version = models.ForeignKey(MenuVersion, on_delete=models.CASCADE, db_index=True, 
                                   related_name='sections',
                                   help_text="The specific version of the menu this section belongs to")
    name = models.CharField(max_length=255, null=False, default='Unnamed Section')

    class Meta:
        unique_together = ['menu_version', 'name']
        indexes = [
            models.Index(fields=['menu_version']),
        ]

    def __str__(self):
        return f"{self.menu_version} - {self.name}"

class MenuItem(models.Model):
    """Represents items in a section"""
    section = models.ForeignKey(MenuSection, on_delete=models.CASCADE, db_index=True, related_name='items')
    name = models.CharField(max_length=255, null=False, db_index=True, default='Unnamed Item')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, db_index=True, default=0.00)

    class Meta:
        indexes = [
            models.Index(fields=['section']),
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]
        unique_together = ['section', 'name']

    def __str__(self):
        return self.name
    
class DietaryRestriction(models.Model):
    """Defines types of dietary restrictions"""
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItemDietaryRestriction(models.Model):
    """Links menu items to their dietary restrictions"""
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    restriction = models.ForeignKey(DietaryRestriction, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ['item', 'restriction']
        indexes = [
            models.Index(fields=['item']),
            models.Index(fields=['restriction']),
        ]

class ProcessingLog(models.Model):
    """Tracks PDF processing operations"""
    menu_version = models.ForeignKey(MenuVersion, on_delete=models.CASCADE, null=True, db_index=True)
    file_name = models.CharField(max_length=255, default='Unnamed File')
    status = models.CharField(max_length=50, db_index=True, default='Pending')
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['menu_version']),
            models.Index(fields=['status']),
            models.Index(fields=['completed_at']),
        ]

    def __str__(self):
        return f"Processing {self.file_name} - {self.status}"
