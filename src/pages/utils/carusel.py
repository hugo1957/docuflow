import flet as ft
import asyncio

def create_carousel(page):
    # Lista de imágenes
    images = [
        {"src": "Autenticacion/1.jpeg", "alt": "Banner 1"},
        {"src": "Autenticacion/2.jpeg", "alt": "Banner 2"},
        {"src": "Autenticacion/3.jpeg", "alt": "Banner 3"},
    ]
    active_index = 0

    # Componente que mostrará la imagen animada
    animated_image = ft.AnimatedSwitcher(
        ft.Container(
            content=ft.Image(
                src=images[0]["src"],
                width="100%",
                height="100%",
                fit=ft.ImageFit.COVER,
            ),
            width=page.width,
            height=150,
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

        # Actualiza el contenido del AnimatedSwitcher
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

    def update_dots():
        # Cambia el color de los "puntitos"
        for i, dot in enumerate(dots.controls):
            dot.bgcolor = "#007BFF" if i == active_index else "#CCCCCC"
        page.update()

    # Bucle asincrónico que actualiza el carrusel cada X segundos
    async def auto_rotate_carousel():
        while True:
            await asyncio.sleep(4)  # Intervalo de rotación en segundos
            update_carousel()

    # Fila de "puntitos" para indicar la imagen activa
    dots = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=10,
                height=10,
                border_radius=50,
                bgcolor="#007BFF" if i == active_index else "#CCCCCC",
                on_click=lambda _, i=i: update_carousel(i),
            )
            for i in range(len(images))
        ],
    )

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

    page.add_async(auto_rotate_carousel())
    
    return carousel
