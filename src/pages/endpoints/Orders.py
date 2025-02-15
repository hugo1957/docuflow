import aiohttp
import asyncio

API_URL = "http://localhost:8000"

async def list_orders(page):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot list orders.")
    return None

  headers = {
    'Accept': 'application/json',
    'Authorization': f'JWT {access_token}'
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/orders/get-orders", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Failed to get orders: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Connection error in list_orders: {e}")
    return None

async def get_order_detail(page,transactionId):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot get order detail.")
    return None

  headers = {
    'Accept': 'application/json',
    'Authorization': f'JWT {access_token}'
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/orders/get-order/{transactionId}", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Failed to get order detail: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Connection error in get_order_detail: {e}")
    return None
