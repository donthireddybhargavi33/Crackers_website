from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal

def format_currency(amount):
    """Format amount as currency"""
    return f"₹{Decimal(amount):.2f}"

import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

def send_order_confirmation(order_data):
    """Send order confirmation email to customer"""
    try:
        subject = 'Order Confirmation - The Mannan Crackers'            
        customer_data = order_data.get('customerData', {})
        
        required_fields = ['fullName', 'email', 'phone', 'deliveryAddress']
        missing_fields = [field for field in required_fields if not customer_data.get(field)]
        
        if missing_fields:
            raise ValidationError(f"Missing required customer data: {', '.join(missing_fields)}")
        
        # Validate email format
        if '@' not in customer_data['email']:
            raise ValidationError("Invalid email format")
        
        # Validate phone number (assuming 10 digits)
        if not customer_data['phone'].isdigit() or len(customer_data['phone']) != 10:
            raise ValidationError("Invalid phone number format")
            
        # Calculate order total and format cart items
        cart_items = order_data['cartItems']
        items_html = ""
        order_total = Decimal('0.00')
        
        for item_id, item in cart_items.items():
            item_price = Decimal(str(item['price']))
            item_quantity = Decimal(str(item['quantity']))
            item_total = item_price * item_quantity
            order_total += item_total
            items_html += f"""
                <tr>
                    <td>{item['name']}</td>
                    <td>{item_quantity}</td>
                    <td>{format_currency(item_price)}</td>
                    <td>{format_currency(item_total)}</td>
                </tr>
            """
            
        # Prepare email context
        context = {
            'customer_name': order_data['customerData']['fullName'],
            'order_total': format_currency(order_total),
            'items_html': items_html,
            'delivery_address': order_data['customerData']['deliveryAddress'],
            'phone': order_data['customerData']['phone'],
            'email': order_data['customerData']['email'],
            'cart_items': cart_items.values()
        }

        # Render email templates
        try:
            html_message = render_to_string('inventory/email/order_confirmation.html', context)
            plain_message = render_to_string('inventory/email/order_confirmation.txt', context)
        except Exception as template_error:
            logger.warning(f"Failed to render email templates: {str(template_error)}. Sending plain text only.")
            html_message = None
            plain_message = f"Order Confirmation\n\nThank you for your order!\n\nOrder Total: {context['order_total']}\nDelivery Address: {context['delivery_address']}"

        # Send email with error handling
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order_data['customerData']['email']],
                html_message=html_message,
                fail_silently=False
            )
            logger.info(f"✅ Order confirmation email sent successfully to {order_data['customerData']['email']}")
            return True
            
        except Exception as smtp_error:
            # Log the error but don't fail the order - email sending is non-critical
            error_msg = str(smtp_error)
            logger.warning(f"⚠️ Failed to send order confirmation email to {order_data['customerData']['email']}: {error_msg}")
            logger.warning(f"Email config - HOST: {settings.EMAIL_HOST}, PORT: {settings.EMAIL_PORT}, USER: {settings.EMAIL_HOST_USER}")
            
            # Return True anyway so checkout completes - email is not critical
            return True
            
    except ValidationError as e:
        logger.error(f"❌ Validation error in order confirmation email: {str(e)}")
        # Don't re-raise - let checkout complete even if validation fails
        return False
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in order confirmation email: {str(e)}")
        # Don't re-raise - let checkout complete
        return False



def send_stock_alert(product):
    """Send low stock alert to admin"""
    try:
        subject = f'Low Stock Alert - {product.name}'
        
        context = {
            'product': product
        }

        # Render email templates with error handling
        try:
            html_message = render_to_string('inventory/email/stock_alert.html', context)
            plain_message = render_to_string('inventory/email/stock_alert.txt', context)
        except Exception as template_error:
            logger.warning(f"Failed to render stock alert templates: {str(template_error)}")
            html_message = None
            plain_message = f"Low Stock Alert\n\nProduct: {product.name}\nCurrent Stock: {product.stock_quantity}"

        # Send email with error handling
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],  # Send to admin email
                html_message=html_message,
                fail_silently=False
            )
            logger.info(f"✅ Stock alert email sent for product: {product.name}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to send stock alert email for {product.name}: {str(e)}")
            # Don't raise - stock alerts are non-critical
            
    except Exception as e:
        logger.error(f"❌ Unexpected error in stock alert email: {str(e)}")
        # Don't raise - stock alerts are non-critical


# =====================================================
# 🔴 ERROR RESPONSE HANDLERS
# =====================================================

from django.http import JsonResponse

def handle_api_error(error_type, message, status_code=400, extra_data=None):
    """
    Generate standardized API error response
    
    error_type: 'validation', 'authentication', 'permission', 'not_found', 'server', 'network'
    message: Error message to display to user
    status_code: HTTP status code
    extra_data: Additional data to include in response
    """
    response_data = {
        'success': False,
        'error': message,
        'error_type': error_type,
        'error_code': status_code,
    }
    
    if extra_data:
        response_data.update(extra_data)
    
    logger.error(f"API Error [{error_type}]: {message}")
    return JsonResponse(response_data, status=status_code)


def get_error_message(error_type):
    """Get user-friendly error message based on error type"""
    messages = {
        'validation': 'The data you provided is invalid. Please check and try again.',
        'authentication': 'You need to log in to perform this action.',
        'permission': 'You don\'t have permission to perform this action.',
        'not_found': 'The requested resource was not found.',
        'server': 'An unexpected error occurred on our servers. Please try again later.',
        'network': 'Network connection error. Please check your internet and try again.',
        'checkout': 'An error occurred during checkout. Please review your information and try again.',
        'payment': 'Payment processing failed. Please try again or contact support.',
        'stock': 'Some items in your cart are no longer available. Please review your order.',
        'minimum_order': 'Minimum order amount not met. Please add more items to your cart.',
    }
    return messages.get(error_type, 'An unexpected error occurred. Please try again.')
