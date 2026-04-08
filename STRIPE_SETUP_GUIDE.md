# Stripe Payment Gateway Integration Guide

## Overview
This e-commerce platform uses Stripe as the payment gateway for secure online payments. The implementation handles order creation, payment processing, and order confirmation.

## Setup Instructions

### 1. Install Required Packages
```bash
pip install -r requirements.txt
```

Or install Stripe specifically:
```bash
pip install stripe==9.8.0
```

### 2. Get Stripe API Keys
1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Sign up for a Stripe account (free)
3. Navigate to Developers → API Keys
4. Copy your **Publishable Key** and **Secret Key**
   - Test keys start with `pk_test_` and `sk_test_`
   - Live keys start with `pk_live_` and `sk_live_`

### 3. Configure Environment Variables
Create a `.env` file in your project root (copy from `.env.example`):
```
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
```

### 4. Database Setup
Ensure you have the following models created (already included):
- `Order` - Store order information
- `OnlinePaymentRequest` - Track payment transactions
- `Cart` - Shopping cart for users
- `CartItem` - Individual items in cart

Run migrations:
```bash
python manage.py migrate
```

## Payment Flow

### Step 1: Add to Cart
User adds products to cart using the `add_to_cart` endpoint.

### Step 2: View Cart
User views cart items at `/backends/cart-items/` and can:
- Update quantities
- Remove items
- View totals with tax and discounts

### Step 3: Checkout
User navigates to `/backends/checkout/` to:
- Enter shipping address
- Enter billing address (or use same as shipping)
- Review order summary
- Click "Continue to Payment"

**Created Order at this stage:**
- Order status: `pending`
- Session stores order ID for payment processing

### Step 4: Payment Processing
User goes to `/backends/payment-process/` where:
1. Stripe Payment Intent is created server-side
2. Stripe Elements card form is displayed
3. User enters card details (never stored on server)
4. Payment is submitted to Stripe
5. Payment Intent is confirmed

**Supported Test Card Numbers:**
- `4242 4242 4242 4242` - Success
- `4000 0000 0000 0002` - Card declined
- `4000 0025 0000 3155` - Requires authentication

Use any future expiry date and any 3-digit CVC.

### Step 5: Payment Confirmation
After successful payment:
1. Payment status is verified with Stripe
2. Order status updated to `processing`
3. `OnlinePaymentRequest` record created
4. Cart is cleared
5. User redirected to confirmation page

### Step 6: Order Confirmation
User sees `/backends/order-confirmation/order_id/` with:
- Order number and details
- Payment confirmation
- Shipping information
- Next steps

## API Endpoints

### Cart Management
- `GET /backends/cart-items/` - View cart items
- `POST /backends/cart-items/` - Update/delete cart items
  - Action: `update`, `delete`
  - Parameters: `cart_item_id`, `quantity` (for update)

### Checkout Flow
- `GET /backends/checkout/` - Display checkout form
- `POST /backends/checkout/` - Create order and submit checkout
  - Parameters: `shipping_address`, `billing_address`, `use_same_address`

### Payment
- `GET /backends/payment-process/` - Display payment form
- `POST /backends/payment-process/` - Create payment intent
  - Returns: `client_secret`, `publishable_key` (JSON)

### Payment Confirmation
- `POST /backends/payment-confirm/` - Confirm payment with server
  - Parameters: `payment_intent_id`, `order_id`
  - Returns: `success`, `redirect_url`, `order_number` (JSON)

### Order Information
- `GET /backends/order-confirmation/<order_id>/` - View order details
- `GET /backends/order-status/<order_id>/` - Get order status (JSON)

## Security Features

1. **PCI Compliance**: Card data never touches your server
   - Stripe Elements handles card input
   - Only Payment Intent ID is stored

2. **CSRF Protection**: All forms use Django's CSRF tokens

3. **Authentication**: All checkout endpoints require login

4. **Payment Verification**: Payment status verified with Stripe before confirming

5. **SSL Encryption**: All transactions use HTTPS

## Database Models

### Order Model
```python
Order(
    customer,           # ForeignKey to Customer
    order_number,      # Auto-generated (ORD20260308customer_id0001)
    shipping_address,  # Full shipping address
    billing_address,   # Full billing address
    status,            # pending, processing, shipped, delivered, cancelled
    tax,               # Tax amount
    shipping_cost,     # Shipping cost
    paid_amount,       # Amount paid
    due_amount,        # Amount still due
    total_amount,      # Total order amount
    points_awarded,    # Loyalty points awarded
)
```

### OnlinePaymentRequest Model
```python
OnlinePaymentRequest(
    order,                # ForeignKey to Order
    transaction_id,       # Stripe Payment Intent ID
    amount,              # Amount charged
    payment_status,      # pending, completed, failed
    created_by,          # User who created the payment
)
```

## Handling Payment Failures

### Client-Side Failures
Users see error messages under the card input indicating:
- Card declined
- Expired card
- Incorrect CVC
- etc.

### Server-Side Failures
- Order remains in `pending` status
- User can retry payment
- No duplicate charges

### Refunds
To refund a payment:
1. Go to Stripe Dashboard
2. Find the payment intent
3. Issue refund through Stripe UI
4. Update order status in database manually (optional)

## Testing

### Test Mode
All Stripe keys in test mode allow free testing with test card numbers.

### Test Workflow
1. Add test products to database
2. Add to cart
3. Go through checkout with `4242 4242 4242 4242`
4. See confirmation page
5. Check Stripe Dashboard for payment

### Load Test Credit Cards
- Email: Confirmed
- Recurring: 4000000000000069
- Network token: 4000000000000010

See [Stripe test cards](https://stripe.com/docs/testing) for complete list.

## Production Deployment

### Before Going Live
1. Update Stripe keys to live keys (`sk_live_`, `pk_live_`)
2. Update `.env` with production keys
3. Set `DEBUG=False`
4. Enable SSL/HTTPS
5. Update `ALLOWED_HOSTS` with production domain
6. Test complete payment flow

### Monitoring
1. Monitor Stripe Dashboard for failed payments
2. Check order statuses in admin panel
3. Review payment logs in `OnlinePaymentRequest` table

## Troubleshooting

### "Stripe API key not set"
- Check `.env` file has `STRIPE_SECRET_KEY`
- Restart Django server after changing `.env`

### "Payment Intent creation failed"
- Check Stripe keys are correct
- Verify amount is in cents (multiply by 100)
- Check order exists in database

### "Card declined"
- Verify using test card numbers
- Check card hasn't expired
- Try different card

### Payment processed but order not updated
- Check `OnlinePaymentRequest` table
- Verify webhook isn't needed (not used in this implementation)
- Check server logs for errors

## Email Notifications

To add email notifications after payment:
1. Configure email backend in `.env`
2. Create `send_order_confirmation_email()` function in `utils.py`
3. Uncomment the email line in `payment_confirm()` view

## Future Enhancements

1. **Webhooks** - Real-time payment updates
2. **Subscriptions** - Recurring billing
3. **Multiple Payment Methods** - Apple Pay, Google Pay
4. **Invoice Generation** - PDF receipts
5. **Email Notifications** - Automated emails
6. **Refunds** - Self-service refund requests
7. **Order Tracking** - Real-time shipping updates

## Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Elements](https://stripe.com/docs/stripe-js/elements/the-card-element)
- [Payment Intents](https://stripe.com/docs/payments/payment-intents)
- [Django Stripe Integration](https://stripe.com/docs/stripe-in-the-classroom/integrations/django)

## Support

For issues or questions:
1. Check Stripe Dashboard logs
2. Review server error logs
3. Check Django admin for order status
4. Contact Stripe support for payment issues
