from django.contrib import admin
from .models import Profile, SaleItem, Sale, Store, Product, Inventory
# Register your models here.

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    readonly_fields = ['total_price']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.calculate_total()


admin.site.register(Profile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Sale)
admin.site.register(SaleItem)