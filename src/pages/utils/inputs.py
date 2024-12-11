
import flet as ft


def create_input_field(label, value=""):
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text(label, style=ft.TextStyle(color="#717171")),
            ft.TextField(
                value=value,
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
                expand=True,
                filled=False,
            )
        ]
    )


def create_dropdown_field(label, options):
    return ft.Column(
        spacing=5,
        expand=True,
        controls=[
            ft.Text(label, style=ft.TextStyle(color="#717171")),
            ft.Dropdown(
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
                options=[ft.dropdown.Option(option) for option in options],
            )
        ]
    )
