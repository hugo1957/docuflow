import flet as ft

class MyInputField(ft.Column):
    def __init__(self, label, value=""):
        super().__init__()
        self.spacing = 5
        self.controls = [
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


class MyDropdownField(ft.Column):
    def __init__(self, label, options):
        super().__init__()
        self.spacing = 5
        self.expand = True
        self.controls = [
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

