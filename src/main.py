import flet as ft
import re
import os
from pages.Tienda.home import ViewHome
# Tienda
from pages.Tienda.ProductDetail import ViewProductDetail
from pages.Tienda.Cart import ViewCart
from pages.Tienda.PaymentSuccess import ViewPaymentSuccess
from pages.Tienda.Checkout import ViewCheckout
from pages.Tienda.Favorites import ViewFavorites
from pages.Tienda.Order import ViewOrders
from pages.Tienda.OrderDetail import ViewOrderDetail


from pages.User import ViewUser
from pages.Domiciliario.RegisterDomi import ViewRegisterDomiciliario
from pages.auth.Login import ViewLogin
from pages.auth.Token import ViewToken
from pages.auth.PageNotFound import PageNotFound
from pages.auth.Profile import ViewProfile
from pages.InitPage import WelcomeView
# Extras
from pages.Extras.Terminos_condiciones import ViewTermsAndConditions
from pages.Extras.Politicas_privacidad import ViewPrivacyPolicy
from pages.Extras.Autorizacion_tratamiento_datos import ViewDataAuthorization
# Data
from pages.data.Registro_civil import ViewRegistroCivil
from pages.data.Salida_menor import ViewRegistroMenores


class ViewManager:
    def __init__(self, page):
        self.page = page
        self.view_cache = {}

    def get_view(self, route, params=None):
        if route in self.view_cache:
            return self.view_cache[route]

        if route == "/":
            view = WelcomeView
        elif route == "/phone-login":
            view = ViewLogin
        elif route == "/token":
            view = ViewToken
        elif route == "/home":
            view = ViewHome
        elif route == "/user":
            view = ViewUser
        elif route == "/profile":
            view = ViewProfile
        elif re.match(r"^/product-detail/.+", route):
            def view(page): return ViewProductDetail(
                page, params.get("product_url"))
        elif route == "/favorites":
            view = ViewFavorites
        elif route == "/cart":
            view = ViewCart
        elif route == "/checkout":
            view = ViewCheckout
        elif route == "/payment-success":
            view = ViewPaymentSuccess
        elif route == "/orders":
            view = ViewOrders
        elif re.match(r"^/order-detail/.+", route):
            def view(page): return ViewOrderDetail(
                page, params.get("order_id"))
        elif route == "/register-domiciliario":
            view = ViewRegisterDomiciliario
        # Data
        elif route == "/registro-civil":
            view = ViewRegistroCivil
        elif route == "/salida-menores":
            view = ViewRegistroMenores
        # Extras
        elif route == "/terms":
            view = ViewTermsAndConditions
        elif route == "/privacy-policy":
            view = ViewPrivacyPolicy
        elif route == "/data-authorization":
            view = ViewDataAuthorization
        else:
            view = PageNotFound

        self.view_cache[route] = view
        return view


def configure_page(page: ft.Page):
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

    def handle_app_event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)

    page.on_app_lifecycle_state_change = handle_app_event



def handle_navigation(page, view_manager, route):
    params = {}
    if re.match(r"^/product-detail/.+", route):
        params["product_url"] = route[len("/product-detail/"):]
    elif re.match(r"^/order-detail/.+", route):
        params["order_id"] = route[len("/order-detail/"):]

    view_cls = view_manager.get_view(route, params)

    page.controls.clear()
    page.appbar = None
    page.navigation_bar = None

    view = view_cls(page)
    page.add(ft.SafeArea(content=view, expand=True))
    page.update()


async def main(page: ft.Page):
    configure_page(page)
    view_manager = ViewManager(page)

    def on_route_change(e):
        handle_navigation(page, view_manager, e.route)

    def on_view_pop(e):
        if page.controls:
            page.controls.pop()
            page.update()

    page.on_route_change = on_route_change
    page.on_view_pop = on_view_pop

    handle_navigation(page, view_manager, page.route)
    




if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")