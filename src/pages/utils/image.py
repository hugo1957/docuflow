import flet as ft

def create_image_with_loader(src, width, height, fit=ft.ImageFit.COVER, border_radius=None):
    # Contenedor inicial con un loader
    placeholder = ft.Container(
        width=width,
        height=height,
        border_radius=border_radius,
        bgcolor="#F0F0F0",  # Color de fondo para indicar que está cargando
        content=ft.ProgressRing(width=30, height=30),
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Imagen que reemplazará el placeholder
    image = ft.Image(
        src=src,
        width=width,
        height=height,
        fit=fit,
        border_radius=border_radius,
    )

    # Contenedor con stack para superponer el loader y la imagen
    return ft.Stack([placeholder, image])
