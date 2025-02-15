import aiohttp
import asyncio

API_URL = "http://localhost:8000"

async def get_payment_total(page,shipping_id, coupon_name):
    """
    Obtiene el total de pago mediante GET a /api/payment/get-payment-total.
    Retorna el JSON si status == 200 y no hay error, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        return None
    headers = {
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/payment/get-payment-total?shipping_id={shipping_id}&coupon_name={coupon_name}",
                headers=headers
            ) as response:
                response_json = await response.json()
                if response.status == 200 and not response_json.get('error'):
                    return response_json
                else:
                    return None
    except aiohttp.ClientError:
        return None

async def process_payment(
    page,
    shipping_id,
    coupon_name,
    full_name,
    address_line_1,
    address_line_2,
    city,
    state_province_region,
    postal_zip_code,
    country_region,
    telephone_number
):
    """
    Procesa el pago mediante POST a /api/payment/make-payment.
    Retorna el JSON si status == 200 y success es True, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        return None
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    body = {
        "shipping_id": shipping_id,
        "coupon_name": coupon_name,
        "full_name": full_name,
        "address_line_1": address_line_1,
        "address_line_2": address_line_2,
        "city": city,
        "state_province_region": state_province_region,
        "postal_zip_code": postal_zip_code,
        "country_region": country_region,
        "telephone_number": telephone_number
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/payment/make-payment",
                json=body,
                headers=headers
            ) as response:
                resp_json = await response.json()
                if response.status == 200 and resp_json.get('success'):
                    return resp_json
                else:
                    return None
    except aiohttp.ClientError:
        print("Error")
        return None