import flet as ft
import asyncio

def create_carousel(page):
    # Lista de imágenes
    images = [
        {"src": "banner/1.png", "alt": "Banner 1"},
        {"src": "Autenticacion/1.jpeg", "alt": "Banner 2"},
        {"src": "banner/2.png", "alt": "Banner 3"},
    ]
    active_index = 0

    animated_image = ft.AnimatedSwitcher(
        ft.Container(
            content=ft.Image(
                src=images[0]["src"],
                width="100%",
                height="100%",
                fit=ft.ImageFit.CONTAIN,  # Ocupa todo el contenedor
            ),
            width="100%",
            height=200,
            border_radius=ft.border_radius.all(15),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        ),
        duration=500,
        transition=ft.AnimatedSwitcherTransition.FADE,
    )

    def update_carousel(index=None):
        nonlocal active_index
        if index is None:
            active_index = (active_index + 1) % len(images)
        else:
            active_index = index
        animated_image.content = ft.Container(
            content=ft.Image(
                src=images[active_index]["src"],
                fit=ft.ImageFit.COVER,
            ),
            width=page.window.width,
            height=200,
            border_radius=ft.border_radius.all(15),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        update_dots()
        page.update()

    def update_dots():
        for i, dot in enumerate(dots.controls):
            dot.bgcolor = "#007BFF" if i == active_index else "#CCCCCC"
        page.update()

    async def auto_rotate_carousel():
        while True:
            await asyncio.sleep(4)  # Intervalo de rotación
            update_carousel()

    dots = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=10,
                height=10,
                border_radius=50,
                bgcolor="#007BFF" if i == active_index else "#CCCCCC",
                on_click=lambda e, i=i: update_carousel(i),
            )
            for i in range(len(images))
        ],
    )

    carousel = ft.Container(
        width=page.window.width,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=page.window.width,
                    height=200,
                    content=animated_image,
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(vertical=10),
                    content=dots,
                ),
            ],
        ),
    )

    # Iniciar el bucle asincrónico para rotar las imágenes
    def start_carousel_rotation():
        asyncio.run(auto_rotate_carousel())

    page.on_view_pop = start_carousel_rotation  # Se inicia cuando se carga la página

    return carousel
