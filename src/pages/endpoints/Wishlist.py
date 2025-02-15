import aiohttp
import asyncio

API_URL = "http://localhost:8000"

async def get_wishlist_items(page):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot get wishlist items.")
    return None

  headers = {
    "Accept": "application/json",
    "Authorization": f"JWT {access_token}"
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/wishlist/wishlist-items", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error getting wishlist items: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Connection error in get_wishlist_items: {e}")
    return None

async def add_wishlist_item(page, product_id):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot add item to wishlist.")
    return None

  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"JWT {access_token}"
  }
  body = {"product_id": product_id}

  try:
    async with aiohttp.ClientSession() as session:
      async with session.post(f"{API_URL}/api/wishlist/add-item", json=body, headers=headers) as response:
        if response.status == 201:
          return await response.json()
        else:
          print(f"Error adding wishlist item: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Connection error in add_wishlist_item: {e}")
    return None

async def get_wishlist_item_total(page):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot get wishlist item total.")
    return None

  headers = {
    "Accept": "application/json",
    "Authorization": f"JWT {access_token}"
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(f"{API_URL}/api/wishlist/get-item-total", headers=headers) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error getting wishlist item total: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Connection error in get_wishlist_item_total: {e}")
    return None

async def remove_wishlist_item(page, product_id):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot remove item from wishlist.")
    return None

  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"JWT {access_token}"
  }
  body = {"product_id": product_id}

  try:
    async with aiohttp.ClientSession() as session:
      async with session.delete(f"{API_URL}/api/wishlist/remove-item", headers=headers, json=body) as response:
        if response.status == 200:
          return await response.json()
        else:
          print(f"Error removing wishlist item: status {response.status}")
          return None
  except aiohttp.ClientError as e:
    print(f"Connection error in remove_wishlist_item: {e}")
    return None

async def clear_wishlist(page):
  access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
  if not access_token:
    print("No access token provided; cannot clear wishlist.")
    return None

  headers = {
    "Accept": "application/json",
    "Authorization": f"JWT {access_token}"
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.delete(f"{API_URL}/api/wishlist/clear-wishlist", headers=headers) as response:
        if response.status == 200:
          return True
        else:
          print(f"Error clearing wishlist: status {response.status}")
          return False
  except aiohttp.ClientError as e:
    print(f"Connection error in clear_wishlist: {e}")
    return None
