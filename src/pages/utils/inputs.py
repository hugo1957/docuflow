
import flet as ft


def create_input_field(label, width=350, height=40):
    return ft.Column(
        controls=[
            ft.Text(label, style=ft.TextStyle(color="#717171")),
            ft.TextField(

                width=width,
                height=height,
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(
                    horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
            )
        ]
    )


def create_dropdown_field(label, options, width=350, height=40):
    return ft.Column(
        controls=[
            ft.Text(label, style=ft.TextStyle(color="#717171")),
            ft.Dropdown(
                width=width,
                height=height,
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(
                    horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
                options=[ft.dropdown.Option(option)
                         for option in options],
            )
        ]
    )
