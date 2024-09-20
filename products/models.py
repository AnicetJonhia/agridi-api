from django.db import models


from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='products/products_images/',blank=True, null=True)
    video = models.FileField(upload_to='products/products_videos/', blank=True, null=True)
    document = models.FileField(upload_to='products/products_documents/', blank=True, null=True)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        return self.name

    @property
    def total_orders(self):
        """Retourne le nombre total de commandes passées pour ce produit."""
        return self.orders.count()



    def decrease_quantity(self, quantity_ordered):
        """Diminue la quantité disponible après une commande."""
        if quantity_ordered <= self.quantity:
            self.quantity -= quantity_ordered
            self.save()
        else:
            raise ValueError("Commande excède la quantité disponible")



