import flet as ft
import os
def create_image_with_loader(src, width, height, fit=ft.ImageFit.COVER, border_radius=None):
  
    placeholder = ft.Container(
        width=width,
        height=height,
        border_radius=border_radius,
        bgcolor="#F0F0F0",
        content=ft.ProgressRing(width=30, height=30),
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    image = ft.Image(
        src=src,
        width=width,
        height=height,
        fit=fit,
        border_radius=border_radius,
    )

    return ft.Stack([placeholder, image])

def get_image_path(relative_path):
    base_path = os.getenv("ASSETS_DIR", "./assets")  # Configura `ASSETS_DIR` al compilar
    return os.path.join(base_path, relative_path)