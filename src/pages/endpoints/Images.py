import aiohttp
import asyncio
API_URL = "http://localhost:8000"


async def image_init(page):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/images/init/",
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None
    except aiohttp.ClientError as e:
        return None


async def images_home(page):
    access_token = page.client_storage.get(
        "creativeferrets.tienda.access_token")
    if not access_token:
        print("No access token provisto; no se pueden obtener las imagenes.")
        return None

    headers = {
        "Accept": "application/json",
        "Authorization": f"JWT {access_token}"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_URL}/api/images/home/",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al obtener imagenes: status {
                          response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error de conexión en get_images: {e}")
        return None
