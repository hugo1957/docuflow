import aiohttp
import asyncio

API_URL = "http://localhost:8000"

async def get_shipping_options():
  headers = {
    'Accept': 'application/json',
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/shipping/get-shipping-options", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error al obtener opciones de envío: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Error de conexión en get_shipping_options: {e}")
    return None

async def get_shipping_list(page):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provisto; no se puede obtener la lista de envíos.")
    return None

  headers = {
    'Accept': 'application/json',
    'Authorization': f'JWT {access_token}',
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/shipping/shipping/list/", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error al obtener la lista de envíos: status {response}")
          return None
  except aiohttp.ClientError as e:
    print(f"Error de conexión en get_shipping_list: {e}")
    return None

async def get_shipping(page,id):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provisto; no se puede obtener el envío.")
    return None

  headers = {
    'Accept': 'application/json',
    'Authorization': f'JWT {access_token}',
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/shipping/shipping/{id}/", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error al obtener el envío: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Error de conexión en get_shipping: {e}")
    return None

async def get_shipping_list_page(page,p):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provisto; no se puede obtener la lista de envíos.")
    return None

  headers = {
    'Accept': 'application/json',
    'Authorization': f'JWT {access_token}',
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/shipping/shipping/list/?p={p}", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error al obtener la lista de envíos: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Error de conexión en get_shipping_list_page: {e}")
    return None
