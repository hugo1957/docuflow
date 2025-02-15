import aiohttp
import asyncio
API_URL = "http://localhost:8000"


async def add_item(page,product_id):
    """
    Agrega un producto al carrito mediante POST a /api/cart/add-item.
    body -> { "product_id": product_id }
    Retorna el JSON si status == 201, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede agregar item al carrito.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    body = {"product_id": product_id}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/cart/add-item",
                json=body,
                headers=headers
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    error_message = await response.text()
                    return {"status": response.status, "error": error_message}
    except aiohttp.ClientError as e:
        return {"status": "connection_error", "error": str(e)}


async def get_items(page):
    """
    Obtiene los items del carrito vía GET a /api/cart/cart-items.
    Retorna el JSON si status == 200, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se pueden obtener los items del carrito.")
        return None

    headers = {
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/cart/cart-items",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al obtener items del carrito: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_items: {e}")
        return None


async def get_total(page):
    """
    Obtiene el total del carrito vía GET a /api/cart/get-total.
    Retorna el JSON si status == 200, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede obtener el total del carrito.")
        return None

    headers = {
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/cart/get-total",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al obtener el total del carrito: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_total: {e}")
        return None


async def get_item_total(page):
    """
    Obtiene el número total de items del carrito vía GET a /api/cart/get-item-total.
    Retorna el JSON si status == 200, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede obtener el total de items.")
        return None

    headers = {
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/cart/get-item-total",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al obtener item_total: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_item_total: {e}")
        return None


async def update_item(page,product_id,count):
    """
    Actualiza la cantidad de un item en el carrito vía PUT a /api/cart/update-item.
    body -> { "product_id": product_id, "count": count }
    Retorna el JSON si status == 200 y no hay error, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede actualizar el item.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    body = {"product_id": product_id, "count": count}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{API_URL}/api/cart/update-item",
                json=body,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await get_items(page)  # Actualizar items en el carrito
                    if data.get("error"):
                        print("Error devuelto por el servidor en update_item")
                        return None
                    return data
                else:
                    print(f"Error al actualizar item: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en update_item: {e}")
        return None


async def remove_item(page,product_id):
    """
    Elimina un item del carrito vía DELETE a /api/cart/remove-item.
    body -> { "product_id": product_id }
    Retorna el JSON si status == 200, de lo contrario None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede eliminar item del carrito.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    body = {"product_id": product_id}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{API_URL}/api/cart/remove-item",
                headers=headers,
                json=body  # En aiohttp podemos usar `json=` en DELETE
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al eliminar item: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en remove_item: {e}")
        return None


async def empty_cart(page):
    """
    Vacía todo el carrito vía DELETE a /api/cart/empty-cart.
    Retorna True si status == 200, de lo contrario False o None.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede vaciar el carrito.")
        return None

    headers = {
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{API_URL}/api/cart/empty-cart",
                headers=headers
            ) as response:
                if response.status == 200:
                    return True
                else:
                    print(f"Error al vaciar el carrito: status {response.status}")
                    return False
    except aiohttp.ClientError as e:
        print(f"Error de conexión en empty_cart: {e}")
        return None


async def synch_cart(page,cart_items):
    """
    Sincroniza el carrito con el backend mediante PUT a /api/cart/synch.
    'cart_items' es una lista de diccionarios con { "product_id": str, "count": int }
    Retorna True si status == 201, de lo contrario False.
    """
    access_token = await page.client_storage.get_async("creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se puede sincronizar el carrito.")
        return False

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    body = {"cart_items": cart_items}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{API_URL}/api/cart/synch",
                json=body,
                headers=headers
            ) as response:
                if response.status == 201:
                    return True
                else:
                    print(f"Error al sincronizar carrito: status {response.status}")
                    return False
    except aiohttp.ClientError as e:
        print(f"Error de conexión en synch_cart: {e}")
        return False
