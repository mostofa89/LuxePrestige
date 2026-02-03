from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'brands'
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    slaug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'categories'
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_review = models.IntegerField(default=0)
    delivery_day_min = models.IntegerField()
    delivery_day_max = models.IntegerField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'products'
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Image for {self.product.name}"
    

    class Meta:
        db_table = 'product_images'
        ordering = ['position']
    

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.category.name}"
    

    class Meta:
        db_table = 'product_categories'


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'attributes'


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    

    class Meta:
        db_table = 'attribute_values'


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value}"
    

    class Meta:
        db_table = 'product_attribute_values'


class Memebership(models.Model):
    level_name = models.CharField(max_length=50)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.level_name
    

    class Meta:
        db_table = 'memberships'


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    membership = models.ForeignKey(Memebership, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'customers'




class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Review for {self.product.name} - {self.rating} stars"
    

    class Meta:
        db_table = 'reviews'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order of {self.quantity} x {self.product.name}"
    

    class Meta:
        db_table = 'orders'
    


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.name
    
    class Meta:
        db_table = 'wishlists'


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.name
    

    class Meta:
        db_table = 'wishlist_items'
    


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
    

    class Meta:
        db_table = 'carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
    

    class Meta:
        db_table = 'cart_items'


class Order(models.Model):
    Order_status = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    shipping_address = models.TextField(max_length=500, null=True, blank=True)
    billing_address = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Order_status, default='pending')
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order ID {self.id} - {self.status}"
    

    class Meta:
        db_table = 'orders'


        def save(self, *args, **kwargs):
            if not self.order_number:
                curent_year = datetime.now().year
                current_month = datetime.now().month
                curent_day = datetime.now().day
                customer_id = self.customer.id
                last_order = Order.objects.all().order_by('id').last()
                increase_number = 1
                new_order = f"ORD{curent_year}{current_month}{curent_day}{customer_id}000{increase_number}"

                while Order.objects.filter(order_number=new_order).exists():
                    increase_number += 1
                    new_order = f"ORD{curent_year}{current_month}{curent_day}{customer_id}000{increase_number}"
                
                self.order_number = new_order

            super().save(*args, **kwargs)


class onlinePayemntRequest(models.Model):
    status = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=status, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Payment Request for Order ID {self.order.id} - {self.payment_status}"
    

    class Meta:
        db_table = 'online_payment_requests'


class DiscountCupon(models.Model):
    code = models.CharField(max_length=20)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code
    

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name
    

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory for {self.product.name}"
    

class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_date = models.DateTimeField()
    delivery_date = models.DateTimeField()

    def __str__(self):
        return f"Shipment for Order ID {self.order.id}"
    

    


    

class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code
    

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)


class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Transaction for Payment ID {self.payment.id} - {self.status}"


class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    return_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f"Return for Order ID {self.order.id}"
    

class Refund(models.Model):
    return_order = models.ForeignKey(Return, on_delete=models.CASCADE)
    refund_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Refund for Return ID {self.return_order.id}"
    


class CustomerSupport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    support_date = models.DateTimeField(auto_now_add=True)
    issue_description = models.TextField()
    resolution_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Customer Support for Order ID {self.order.id} - {self.resolution_status}"
    

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    


class GiftCard(models.Model):
    code = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code
    


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    featured_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Featured: {self.product.name}"
    


class BestSeller(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sold_quantity = models.IntegerField()

    def __str__(self):
        return f"Best Seller: {self.product.name} - {self.sold_quantity} sold"
    


class NewArrival(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    arrival_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New Arrival: {self.product.name}"
    


class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Flash Sale: {self.product.name} - {self.discount_percentage}% off"
    


class BundleDeal(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    bundle_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    


class LoyaltyProgram(models.Model):
    customer_name = models.CharField(max_length=100)
    points_earned = models.IntegerField()
    membership_level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer_name} - {self.membership_level}"
    

class GiftWrapOption(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class SocialMediaIntegration(models.Model):
    platform_name = models.CharField(max_length=100)
    profile_url = models.URLField()

    def __str__(self):
        return self.platform_name
    

class AnalyticsTracking(models.Model):
    tracking_id = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.tracking_id
    

