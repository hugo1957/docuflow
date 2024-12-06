import re
import flet as ft
import os
from functools import lru_cache
from pages.home import ViewHome
from pages.auth.Profile import ViewProfile
from pages.ProductDetail import ViewProductDetail
from pages.Cart import ViewCart
from pages.auth.PageNotFound import PageNotFound
from pages.PaymentSuccess import ViewPaymentSuccess
from pages.Checkout import ViewCheckout
from pages.auth.Login import ViewLogin
from pages.auth.Token import ViewToken

async def main(page: ft.Page):
    page.adaptive = False
    
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.window.always_on_top = True
    page.padding = ft.padding.all(0)

    def event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)

    page.on_app_lifecycle_state_change = event

    async def show_loader():
        loader = ft.Container(
            content=ft.ProgressRing(width=50, height=50, stroke_width=5),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.TRANSPARENT)
        )
        page.overlay.append(loader)
        page.update()

    async def hide_loader():
        if page.overlay:
            page.overlay.pop()
            page.update()

    @lru_cache(maxsize=None)
    async def load_view(view_function):
        await show_loader()
        try:
            # await asyncio.sleep(0.1)  # Breve retardo para simular carga
            view_function()
        finally:
            await hide_loader()

    async def handle_navigation(route):
        page.controls.clear()
        if route == "/":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewLogin(page), expand=True)))
        elif route == "/token":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewToken(page), expand=True)))
        elif route == "/home":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewHome(page), expand=True)))
        elif route == "/profile":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewProfile(page), expand=True)))
        elif re.match(r"^/product-detail/.+", route):
            # Extraer el parámetro 'url' de la ruta
            product_url = route[len("/product-detail/"):]
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewProductDetail(page, product_url), expand=True)))
        elif route == "/cart":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewCart(page), expand=True)))
        elif route == "/checkout":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewCheckout(page), expand=True)))
        elif route == "/payment-success":
            await load_view(lambda: page.add(ft.SafeArea(
                content=ViewPaymentSuccess(page), expand=True)))
        else:
            await load_view(lambda: page.add(ft.SafeArea(
                content=PageNotFound(page), expand=True)))
        page.update()

    async def route_change(e):
        await handle_navigation(e.route)

    async def view_pop(e):
        if page.controls:
            page.controls.pop()
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await handle_navigation(page.route)



if __name__ == "__main__":
    ft.app(target=main,assets_dir="assets",port=8550,view=ft.WEB_BROWSER)
