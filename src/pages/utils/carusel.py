import asyncio
import flet as ft
from pages.endpoints.Images import images_home

API_URL = "http://localhost:8000"

def create_carousel(page):
    images = []
    active_index = 0

    animated_image = ft.AnimatedSwitcher(
        ft.Container(width=page.width, height=150),
        duration=500,
        transition=ft.AnimatedSwitcherTransition.FADE,
    )

    dots = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[])

    carousel = ft.Container(
        width=page.width,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(15),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=page.width,
                    height=150,
                    content=animated_image,
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=5,
                        color="rgba(0,0,0,0.2)",
                    ),
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(vertical=10),
                    content=dots,
                ),
            ],
        ),
    )

    def update_dots():
        for i, dot in enumerate(dots.controls):
            dot.bgcolor = "#007BFF" if i == active_index else "#CCCCCC"

    def update_carousel(index=None):
        nonlocal active_index
        if not images:
            return
        if index is None:
            active_index = (active_index + 1) % len(images)
        else:
            active_index = index

        animated_image.content = ft.Container(
            content=ft.Image(
                src=images[active_index]["src"],

                fit=ft.ImageFit.COVER,
            ),
            width=page.width,
            height=150,
            border_radius=ft.border_radius.all(15),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        update_dots()
        page.update()

    async def auto_rotate_carousel():
        while True:
            await asyncio.sleep(4)
            update_carousel()

    async def fetch_images_home():
        data = await images_home(page)
        if data and isinstance(data, list):
            for item in data:
                full_url = f"{API_URL}{item['image']}"
                images.append({"src": full_url, "alt": item.get("alt", "")})
            if images:
                dots.controls[:] = [
                    ft.Container(
                        width=10,
                        height=10,
                        border_radius=50,
                        bgcolor="#007BFF" if i == 0 else "#CCCCCC",
                        on_click=lambda e, i=i: update_carousel(i),
                    )
                    for i in range(len(images))
                ]
                update_carousel(0)
                page.run_task(auto_rotate_carousel)
            else:
                print("No hay imágenes que mostrar.")
        else:
            print("La API no devolvió imágenes o result fue None.")

    asyncio.run(fetch_images_home())
    return carousel
  
  
  
# import asyncio
# import flet as ft
# from pages.endpoints.Images import images_home

# API_URL = "http://localhost:8000"

# def create_carousel(page):
#   images = []

#   images_row = ft.Row(
#     controls=[],
#     spacing=10,
#     scroll=ft.ScrollMode.HIDDEN,
#   )

#   carousel = ft.Container(
#     alignment=ft.alignment.center,
#     border_radius=ft.border_radius.all(15),
#     clip_behavior=ft.ClipBehavior.NONE,
#     content=images_row,
#   )

#   async def fetch_images_home():
#     data = await images_home(page)
#     if data and isinstance(data, list):
#       for item in data:
#         full_url = f"{API_URL}{item['image']}"
#         image_container = ft.Container(
#           width=280,
#           height=160,
#           border_radius=ft.border_radius.all(15),
#           clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
#           content=ft.Image(
#             src=full_url,
#             fit=ft.ImageFit.COVER,
#           ),
#           on_click=lambda e, img=full_url: print(f"Seleccionaste {img}"),
#         )
#         images_row.controls.append(image_container)
#       page.update()
#     else:
#       print("La API no devolvió imágenes o result fue None.")

#   asyncio.run(fetch_images_home())

#   return carousel

