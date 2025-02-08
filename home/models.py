from django.db import models

"""class SalesData(models.Model):
    date = models.DateField() 
    customer_id = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(null=True)
    product_category = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    # Bisa tambahkan field lainnya sesuai kebutuhan


    def __str__(self):
        return f"{self.product_category} - {self.date}"
"""
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

