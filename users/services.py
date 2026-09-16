import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY





def create_stripe_product(name="Gold Plan"):
    """Создает продукт и возвращает его объект"""
    return stripe.Product.create(name=name)




def create_stripe_price(amount, product_id):
    """Создает цену для переданного ID продукта"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product_id,
    )



def create_stripe_session(price_id):

    """Создание сессии на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8001/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )

    return  session.id, session.url