from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F, ExpressionWrapper, DecimalField



class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='profiles')

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} in {self.store.name}"


class Sale(models.Model):
    """
    Sale model representing a completed transaction.
    
    Best Practices:
    - related_name for reverse lookups
    - Default value for total_price to prevent NULL issues
    - Large max_digits for total_price to handle large orders
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sales')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sales')
    total_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.sale_date.strftime('%Y-%m-%d %H:%M')} - {self.total_price}"

    def calculate_total(self):
        """
        Recalculate total price from all sale items using database-level aggregation.
        
        Performance: Uses Django ORM aggregation for efficient calculation.
        """
        #self.items refers to the reverse ForeignKey relation from the SaleItem model back to the Sale model.
        total = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('quantity') * F('unit_price'),
                    output_field=DecimalField(max_digits=12, decimal_places=2)
                )
            )
        )['total'] or Decimal('0.00')
        
        self.total_price = total
        self.save(update_fields=['total_price'])
        return total


class SaleItem(models.Model):
    #The key part is related_name='items'. This tells Django: "When accessing this relationship from the Sale side, use the name items."
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.unit_price}"