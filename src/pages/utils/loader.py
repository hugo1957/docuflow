# pages/utils/controls/Loader.py

import flet as ft

def create_loader():
    loader = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.WHITE.with_opacity(0.8),
        content=ft.Column(
            [
                ft.ProgressRing(scale=3, color="#FF5700"),
                ft.Text("Cargando...", size=16, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )
    return loader
