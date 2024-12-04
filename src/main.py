from pages.utils.inputs import create_input_field, create_dropdown_field
import datetime
from threading import Timer
from pages.utils.alert import show_construction_dialog
import re
import flet as ft
import os
from functools import lru_cache
import threading
from pages.home import ViewHome
from pages.utils.json import json_base64
from pages.utils.navigation import create_footer
from pages.auth.Profile import ViewProfile



def main(page: ft.Page):
    page.adaptive = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.window.always_on_top = True
    # page.session.set("api_url", "https://app.latirculm.com")
    # page.fonts = {
    #     "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
    # }
    # page.theme = ft.Theme(
    #     primary_color_dark="black",
    #     primary_color_light="white",
    # )
    page.padding = ft.padding.all(0)

    def event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)
    page.on_app_lifecycle_state_change = event

    def show_loader():
        loader = ft.Container(
            content=ft.ProgressRing(width=50, height=50, stroke_width=5),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.TRANSPARENT)
        )
        page.overlay.append(loader)
        page.update()

    def hide_loader():
        if page.overlay:
            page.overlay.pop()
            page.update()

    @lru_cache(maxsize=None)
    def load_view(view_function):
        timer = threading.Timer(0.5, show_loader)
        timer.start()

        def wrapper():
            view_function()
            timer.cancel()
            hide_loader()

        threading.Thread(target=wrapper).start()

    def handle_navigation(route):
        page.controls.clear()

        if route == "/":
            load_view(lambda: page.add(ft.SafeArea(
                content=ViewHome(page), expand=True)))
        elif route == "/profile":
            load_view(lambda: page.add(ft.SafeArea(
                content=ViewProfile(page), expand=True)))

        page.update()

    def route_change(e):
        handle_navigation(e.route)

    def view_pop(e):
        page.controls.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


def ViewProfile(page):
    page.controls.clear()
    page.navigation_bar = create_footer(page)

    name_field = create_input_field("Nombres")
    last_name_field = create_input_field("Apellidos")
    document_field = create_input_field("Número de Identificación")
    email_field = create_input_field("E-mail")
    phone_field = create_input_field("Celular")
    register_number_field = create_input_field("Número de Registro Civil")
    city_field = create_input_field("Ciudad expedición")
    deparment_field = create_input_field("Departamento")
    notaria_registraduria = create_input_field("Notaria, Numero ó Registraduria")
    def on_date_change(e):
        selected_date = e.control.value.strftime("%Y-%m-%d")
        birth_date_field.value = selected_date
        page.update()

    birth_date_field = ft.Column(
        controls=[
            ft.Text("Fecha de Nacimiento",
                    style=ft.TextStyle(color="#717171")),
            ft.TextField(
                width=300,
                height=40,
                border_radius=ft.border_radius.all(15),
                content_padding=ft.padding.symmetric(
                    horizontal=20, vertical=15),
                bgcolor=ft.Colors.WHITE,
                border_color="#717171",
                label_style=ft.TextStyle(color="#717171"),
                border_width=0.5,
                value="",
            )
        ]
    )

    # Contenedor principal
    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Column(
                          expand=True,
                            scroll=ft.ScrollMode.HIDDEN,
                            spacing=5,
                            controls=[
                                ft.Container(height=5),
                                ft.Text(
                                    "Mi Perfil", text_align="left", size=20, weight="bold"),
                                ft.Container(height=5),
                                name_field,
                                last_name_field,
                                document_field,
                                email_field,
                                phone_field,
                                ft.Row(
                                    controls=[
                                        birth_date_field,
                                        ft.IconButton(
                                            icon=ft.Icons.CALENDAR_MONTH,
                                            on_click=lambda e: page.open(
                                                ft.DatePicker(
                                                    first_date=datetime.datetime(
                                                        year=2023, month=10, day=1),
                                                    last_date=datetime.datetime(
                                                        year=2024, month=10, day=1),
                                                    on_change=on_date_change,
                                                )
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Container(height=5),
                                ft.Text(
                                    "Para mas DocuFlow", text_align="left", size=20, weight="bold"),
                                register_number_field,
                                city_field,
                                deparment_field,
                                notaria_registraduria,
                            ]
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            # on_click=handle_login_click,
                            ink=True,
                            border_radius=ft.border_radius.all(35),
                            width=350,
                            height=40,
                            bgcolor="#25D366",
                            content=ft.Text(
                                "Guardar", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                    ]
                )
            )
        ]
    )

    return container
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
