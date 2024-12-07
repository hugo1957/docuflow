import flet as ft
import re
import os
from pages.home import ViewHome
from pages.auth.Profile import ViewProfile
from pages.ProductDetail import ViewProductDetail
from pages.Cart import ViewCart
from pages.auth.PageNotFound import PageNotFound
from pages.PaymentSuccess import ViewPaymentSuccess
from pages.Checkout import ViewCheckout
from pages.auth.Login import ViewLogin
from pages.auth.Token import ViewToken
from pages.Favorites import ViewFavorites
from pages.Order import ViewOrders
from pages.OrderDetail import ViewOrderDetail


class ViewManager:
    def __init__(self, page):
        self.page = page
        self.view_cache = {}
        
    def get_view(self, route, params=None):
        if route in self.view_cache:
            return self.view_cache[route]

        if route == "/":
            view = ViewLogin(self.page)
        elif route == "/token":
            view = ViewToken(self.page)
        elif route == "/home":
            view = ViewHome(self.page)
        elif route == "/profile":
            view = ViewProfile(self.page)
        elif re.match(r"^/product-detail/.+", route):
            product_url = params.get("product_url")
            view = ViewProductDetail(self.page, product_url)
        elif route == "/favorites":
            view = ViewFavorites(self.page)
        elif route == "/cart":
            view = ViewCart(self.page)
        elif route == "/checkout":
            view = ViewCheckout(self.page)
        elif route == "/payment-success":
            view = ViewPaymentSuccess(self.page)
        elif route == "/orders":
            view = ViewOrders(self.page)
        elif re.match(r"^/order-detail/.+", route):
            order_id = params.get("order_id")
            view = ViewOrderDetail(self.page, order_id)
        else:
            view = PageNotFound(self.page)

        self.view_cache[route] = view
        return view


async def main(page: ft.Page):
    page.adaptive = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.padding = ft.padding.all(0)
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.window.always_on_top = True
    def event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)

    page.on_app_lifecycle_state_change = event

    view_manager = ViewManager(page)

    def handle_navigation(route):
        page.controls.clear()
        
        params = {}
        if re.match(r"^/product-detail/.+", route):
            params["product_url"] = route[len("/product-detail/"):]
        elif re.match(r"^/order-detail/.+", route):
            params["order_id"] = route[len("/order-detail/"):]

        view = view_manager.get_view(route, params)
        page.add(ft.SafeArea(content=view, expand=True))
        page.update()

    def route_change(e):
        handle_navigation(e.route)

    def view_pop(e):
        if page.controls:
            page.controls.pop()
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    handle_navigation(page.route)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
