import aiohttp
import requests
import flet as ft

API_URL = "http://localhost:8000"

async def get_categories():
    """
    Obtiene la lista de categorías desde el endpoint /api/category/categories
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/category/categories",
                headers={"Accept": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Error al obtener categorías: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_categories: {e}")
        return None


async def get_products():
    """
    Obtiene la lista de productos desde el endpoint /api/product/get-products
    (se quita el uso de dispatch).
    """
    config = {
        "headers": {
            "Accept": "application/json"
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/product/get-products",
                headers=config["headers"]
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Error al obtener productos: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_products: {e}")
        return None


async def get_product_detail(page, id):
    """
    Llama a /api/product/product/<slug> para obtener el detalle de un producto.
    Retorna el JSON con la información si el status == 200, de lo contrario None.
    """
    # En caso de requerir autenticación, obtén el token o credenciales:
    # access_token = page.client_storage.get_async("some_token")
    # headers = {
    #    "Authorization": f"Bearer {access_token}" 
    # }
    # Asumamos que este endpoint no necesita token, sino que es público:
    headers = {
        "Accept": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/product/product/{id}",
                headers=headers
            ) as response:
                if response.status == 200:

                    return await response.json()
                else:
                    print(f"Error al obtener producto con slug={id}: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_product_detail: {e}")
        return None
      
async def get_filtered_products(category_id, price_range, sort_by, order):
    """
    Obtiene productos filtrados a través del endpoint /api/product/by/search,
    enviando un body con los filtros en formato JSON.
    """
    body = {
        "category_id": category_id,
        "price_range": price_range,
        "sort_by": sort_by,
        "order": order
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/product/by/search",
                json=body,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Verificamos si el back envía un "error" en data
                    if not data.get("error"):
                        return data
                    else:
                        print("Error devuelto por el servidor en get_filtered_products")
                        return None
                else:
                    print(f"Error al filtrar productos: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_filtered_products: {e}")
        return None


async def get_search_products(search, category_id):
    """
    Busca productos usando el endpoint /api/product/search,
    enviando 'search' y 'category_id' en el body (JSON).
    """
    body = {
        "search": search,
        "category_id": category_id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/product/search",
                json=body,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al buscar productos: status {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_search_products: {e}")
        return None



async def fetch_and_cache_categories(page):
    try:
        result_categories = await get_categories()
        if result_categories:
            await page.client_storage.set_async(
                "creativeferrets.tienda.categories", result_categories)
            return result_categories
    except Exception as e:
        print(f"Error fetching categories: {e}")

async def fetch_and_cache_products(page):
    try:
        result_products = await get_products()
        if result_products:
            await page.client_storage.set_async(
                "creativeferrets.tienda.products", result_products)
            return result_products
    except Exception as e:
        print(f"Error fetching products: {e}")

async def update_cache_in_background(page, cache_key, fetch_function):
    try:
        result = await fetch_function(page)
        if result:
            await page.client_storage.set_async(cache_key, result)
    except Exception as e:
        print(f"Error updating cache {cache_key}: {e}")

