import aiohttp
import asyncio

API_URL = "http://localhost:8000"

async def check_coupon(page,coupon_name):
  """
  Verifica un cupón mediante GET a /api/coupons/check-coupon.
  Retorna el JSON si status == 200, de lo contrario None.
  """
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provisto; no se puede verificar el cupón.")
    return None

  headers = {
    "Accept": "application/json",
    "Authorization": f"JWT {access_token}"
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(
        f"{API_URL}/api/coupons/check-coupon?coupon_name={coupon_name}",
        headers=headers
      ) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error al verificar cupón: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Error de conexión en check_coupon: {e}")
    return None

# Ejemplo de uso
# asyncio.run(check_coupon("NOMBRE_DEL_CUPON"))
