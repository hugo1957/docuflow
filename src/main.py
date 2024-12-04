
import re
import flet as ft
import os
from functools import lru_cache
import threading
from pages.home import ViewHome
from pages.utils.json import json_base64
from pages.utils.navigation import create_footer
from pages.auth.Profile import ViewProfile
from pages.ProductDetail import ViewProductDetail


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
        elif route == "/product-detail":
            page.add(ft.SafeArea(
                content=ViewProductDetail(page), expand=True))
        page.update()

    def route_change(e):
        handle_navigation(e.route)

    def view_pop(e):
        page.controls.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)



if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
