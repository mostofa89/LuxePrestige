# 🚀 Quick Start - Checkout & Payment

## Installation (5 minutes)

```bash
# 1. Install Stripe
pip install stripe

# Or if using requirements.txt
pip install -r requirements.txt

# 2. Get Stripe Keys
# Visit: https://dashboard.stripe.com/apikeys

# 3. Update .env file
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_public_key

# 4. Run migrations (if any new models)
python manage.py migrate

# 5. Start server
python manage.py runserver
```

## Test Payment Flow (2 minutes)

```
1. Go to http://localhost:8000/backends/product/
2. Add a product to cart
3. Go to http://localhost:8000/backends/cart-items/
4. Click "Proceed to Checkout"
5. Enter random shipping address
6. Use billing = shipping address
7. Click "Continue to Payment"
8. Enter Card: 4242 4242 4242 4242
9. Any future date (e.g., 12/28)
10. Any 3-digit CVC (e.g., 123)
11. See confirmation page!
```

## Files Summary

```
NEW ENDPOINTS:
├── GET/POST  /backends/checkout/
├── GET/POST  /backends/payment-process/
├── POST      /backends/payment-confirm/
├── GET       /backends/order-confirmation/<id>/
└── GET       /backends/order-status/<id>/

NEW VIEWS (backends/views.py):
├── checkout()
├── payment_process()
├── payment_confirm()
├── order_confirmation()
└── order_status()

NEW TEMPLATES:
├── templates/backends/checkout.html
├── templates/backends/payment.html
└── templates/backends/order_confirmation.html

DOCUMENTATION:
├── STRIPE_SETUP_GUIDE.md
├── PAYMENT_IMPLEMENTATION.md
└── CHECKOUT_PAYMENT_SUMMARY.md
```

## API Testing (with curl)

```bash
# Get order status
curl http://localhost:8000/backends/order-status/1/

# Response:
{
  "order_id": 1,
  "order_number": "ORD20260308customer_id0001",
  "status": "processing",
  "total_amount": 99.99,
  "paid_amount": 99.99,
  "due_amount": 0.0,
  "payment_status": "completed"
}
```

## Database Models Used

```python
# Already in your database:
Order                   # Master order record
OnlinePaymentRequest    # Payment transactions
Cart                    # Shopping cart
CartItem                # Individual items
Customer                # User profile with membership
```

## Key Code Snippets

### Accessing order in template
```django
{{ order.order_number }}
{{ order.total_amount|floatformat:2 }}
{{ order.get_status_display }}
```

### Getting customer discount
```python
customer = Customer.objects.get(customer=request.user)
discount = customer.membership.discount_percentage if customer.membership else 0
```

### Creating payment intent
```python
stripe.PaymentIntent.create(
    amount=int(total * 100),  # Amount in cents
    currency='usd',
    description=f'Order {order.order_number}'
)
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `stripe.error.AuthenticationError` | Check `.env` STRIPE_SECRET_KEY |
| `ModuleNotFoundError: stripe` | Run `pip install stripe` |
| Card declined in test | Use `4242 4242 4242 4242` |
| Amount mismatch | Ensure multiply by 100 for cents |
| Order not created | Check database migrations |

## Test Card Numbers

| Type | Card | Exp | CVC |
|------|------|-----|-----|
| Success | 4242 4242 4242 4242 | Any future | Any 3-digit |
| Declined | 4000 0000 0000 0002 | Any future | Any 3-digit |
| 3D Secure | 4000 0025 0000 3155 | Any future | Any 3-digit |

## Deployed URLs (when live)

```
Checkout:      https://your-domain.com/backends/checkout/
Payment:       https://your-domain.com/backends/payment-process/
Confirmation:  https://your-domain.com/backends/order-confirmation/1/
```

## Environment Variables

```env
# Required
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Optional (for email)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

## Stripe Dashboard

- **Payments**: https://dashboard.stripe.com/payments
- **Customers**: https://dashboard.stripe.com/customers
- **API Keys**: https://dashboard.stripe.com/apikeys
- **Documentation**: https://stripe.com/docs

## Useful Django Commands

```bash
# Check migrations
python manage.py showmigrations

# Create superuser (if needed)
python manage.py createsuperuser

# Access Django shell
python manage.py shell
>>> from backends.models import Order
>>> Order.objects.all()

# Run specific migration
python manage.py migrate backends
```

## Production Checklist

- [ ] Stripe keys are production keys (`sk_live_`, `pk_live_`)
- [ ] DEBUG=False in settings
- [ ] ALLOWED_HOSTS updated
- [ ] SSL certificate installed
- [ ] Database backed up
- [ ] Email configured
- [ ] Tested full payment flow once

## Performance Tips

1. Use `select_related()` for foreign keys
2. Use `prefetch_related()` for many-to-many
3. Cache order status
4. Index frequently queried fields

## Security Reminders

- Never log card numbers
- Never hardcode API keys
- Use HTTPS in production
- Validate all user input
- Regenerate SECRET_KEY for production
- Use environment variables

## Support & Debugging

```bash
# Check server logs
tail -f server.log

# Django debug
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)

# Test Stripe connectivity
python manage.py shell
>>> import stripe
>>> stripe.api_key = "sk_test_..."
>>> stripe.Account.retrieve()
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure Stripe keys
3. ✅ Test payment flow
4. ✅ Deploy to production
5. ✅ Monitor orders
6. 🔄 Add email notifications (optional)
7. 🔄 Setup order tracking (optional)
8. 🔄 Create admin dashboard (optional)

---

**Need Help?**
- See STRIPE_SETUP_GUIDE.md for detailed setup
- Check Stripe docs: stripe.com/docs
- Review server logs for errors
