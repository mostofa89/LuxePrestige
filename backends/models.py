from datetime import datetime
from decimal import Decimal, ROUND_DOWN
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
    slug = models.SlugField(unique=True)
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
    weight = models.DecimalField(max_digits=10, decimal_places=2)
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


class Membership(models.Model):
    TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    ]
    name = models.CharField(max_length=100, default='Standard Membership')
    tier = models.CharField(max_length=50, choices=TIER_CHOICES)
    description = models.TextField(blank=True)
    benefits = models.TextField(blank=True, help_text="Enter each benefit on a new line")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'memberships'
        constraints = [
            models.UniqueConstraint(fields=['tier'], name='unique_membership_tier')
        ]


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    points = models.IntegerField(default=0)
    points_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'customers'

    def get_tier_from_points(self):
        if self.points >= 40000:
            return 'diamond', Decimal('15.00')
        if self.points >= 30000:
            return 'platinum', Decimal('11.00')
        if self.points >= 20000:
            return 'gold', Decimal('7.00')
        if self.points >= 10000:
            return 'silver', Decimal('3.00')
        return 'bronze', Decimal('0.00')


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


class MenuList(models.Model):
    module_name = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=100)
    menu_url = models.CharField(max_length=255)
    menu_icon = models.CharField(max_length=100, null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    is_main_menu = models.BooleanField(default=False)
    is_sub_menu = models.BooleanField(default=False)
    is_sub_child_menu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    


    def __str__(self):
        return self.menu_name
    

    class Meta:
        db_table = 'menulist'


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuList, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Created_by_user')
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Deleted_by_user')
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Permissions for {self.user.username}"
    

    class Meta:
        db_table = 'user_permissions'


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Wishlist for {self.customer.name}"
    
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Cart for {self.customer.name}"
    

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
    STATUS_CHOICES = [
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    points_awarded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return f"Order ID {self.id} - {self.status}"
    

    class Meta:
        db_table = 'orders'

    def _calculate_points_from_paid_amount(self):
        if not self.paid_amount:
            return 0
        return int((self.paid_amount * Decimal('10')).quantize(Decimal('1'), rounding=ROUND_DOWN))

    def _apply_points_to_customer(self, points):
        if points <= 0:
            return
        customer = self.customer
        customer.points = (customer.points or 0) + points
        tier, discount = customer.get_tier_from_points()
        membership = Membership.objects.filter(tier=tier, is_active=True).order_by('id').first()

        update_fields = ['points']
        if membership and customer.membership_id != membership.id:
            customer.membership = membership
            update_fields.append('membership')
        if customer.points_discount_percentage != discount:
            customer.points_discount_percentage = discount
            update_fields.append('points_discount_percentage')

        customer.save(update_fields=update_fields + ['updated_at'])

    def save(self, *args, **kwargs):
        if not self.order_number:
            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day
            customer_id = self.customer.id
            increase_number = 1
            new_order = f"ORD{current_year}{current_month}{current_day}{customer_id}000{increase_number}"

            while Order.objects.filter(order_number=new_order).exists():
                increase_number += 1
                new_order = f"ORD{current_year}{current_month}{current_day}{customer_id}000{increase_number}"

            self.order_number = new_order

        points_to_award = 0
        if self.status == 'delivered' and self.points_awarded == 0:
            previous = None
            if self.pk:
                previous = Order.objects.filter(pk=self.pk).values('status', 'points_awarded').first()
            prev_status = previous['status'] if previous else None
            prev_awarded = previous['points_awarded'] if previous else 0
            if prev_status != 'delivered' and prev_awarded == 0:
                points_to_award = self._calculate_points_from_paid_amount()
                self.points_awarded = points_to_award

        super().save(*args, **kwargs)

        if points_to_award:
            self._apply_points_to_customer(points_to_award)


class CancelledOrder(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Cancelled Order ID {self.order.id} - {self.get_status_display()}"
    

    class Meta:
        db_table = 'cancelled_orders'


class OnlinePaymentRequest(models.Model):
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


class DiscountCoupon(models.Model):
    code = models.CharField(max_length=20)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.code
    

    class Meta:
        db_table = 'discount_coupons'
    

    

class OrderReturn(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Return for Order ID {self.order.id}"
    

    class Meta:
        db_table = 'order_returns'


class Refund(models.Model):
    return_order = models.ForeignKey(OrderReturn, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    refund_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Refund for Return ID {self.return_order.id}"
    

    class Meta:
        db_table = 'refunds'



class CustomerSupport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    support_date = models.DateTimeField(auto_now_add=True)
    issue_description = models.TextField()
    resolution_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Customer Support for Order ID {self.order.id} - {self.resolution_status}"
    

    class Meta:
        db_table = 'customer_supports'



class CustomerSupportTicket(models.Model):
    support = models.OneToOneField(CustomerSupport, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=100)
    issue_details = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Support Ticket {self.ticket_number} - {self.status}"
    


    class Meta:
        db_table = 'customer_support_tickets'


class ServerCustomerSupportChat(models.Model):
    support = models.OneToOneField(CustomerSupport, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=50)

    def __str__(self):
        return f"Chat Message from {self.sender} at {self.sent_at}"
    

    class Meta:
        db_table = 'customer_support_chats'


class CustomerSupportFeedback(models.Model):
    support = models.OneToOneField(ServerCustomerSupportChat, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Feedback for Support ID {self.support.id} - {self.rating} stars"
    


    class Meta:
        db_table = 'customer_support_feedbacks'



class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    restock_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Inventory for {self.product.name} - {self.stock_quantity} in stock"
    

    class Meta:
        db_table = 'inventories'
    


    


    

