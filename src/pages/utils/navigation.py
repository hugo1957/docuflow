import flet as ft
import flet_lottie as fl
from pages.endpoints.Cart import get_items

# Helper para obtener índice del footer según la ruta
def get_footer_selected_index(route):
    route_to_index = {
        "/home": 0,
        "/user": 1,
        "/contacto": 3,
    }
    return route_to_index.get(route, 0)

# Helper para obtener ruta desde índice del footer
def get_route_from_index(page, index):
    footer_routes = [
        "/home",
        "/user",
        "/favorites",
        "/contacto",
    ]
    return footer_routes[index] if index < len(footer_routes) else "/home"

# NAVBAR PRINCIPAL (por ejemplo, para la Home)
def create_navbar_home(page):
    """
    Devuelve:
      1) Un AppBar con un icono de carrito que muestra la cantidad de items.
      2) Una función update_cart_count() que, al llamarse, consulta el carrito en 2do plano.
    """

    # Texto que muestra la cuenta de productos en el carrito
    cart_count = ft.Text(
        value="0",
        color="white",
        size=12,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Función para actualizar el contador de manera ASÍNCRONA
    async def fetch_cart_count():
      items = await get_items(page)
      cart_count.value = str(len(items["cart"])) if items and "cart" in items else "0"
      try:
          cart_count.update()
      except AssertionError:
          # Ya no está en el árbol, ignoramos
          pass


    # Función que se invoca desde la app para actualizar el contador
    def update_cart_count():
        # Lanza la corrutina en 2do plano, sin bloquear la UI
        page.run_task(fetch_cart_count)

    cart_icon = ft.Container(
        content=ft.Stack(
            [
                fl.Lottie(
                    src="https://creativeferrets.com/assets/lottie/cart.json",
                    animate=True,
                    width=30,
                    height=30,
                ),
                ft.Container(
                    content=cart_count,
                    bgcolor="red",
                    border_radius=ft.border_radius.all(12),
                    alignment=ft.alignment.center,
                    width=20,
                    height=20,
                    offset=ft.Offset(0.8, -0.6),
                ),
            ]
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(15),
        on_click=lambda e: page.go("/cart"),
    )

    nav_bar = ft.AppBar(
        title=ft.Text("DocuFlow", color="white"),
        bgcolor="#007354",
        actions=[cart_icon],
        elevation=0,
        elevation_on_scroll=0,
    )

    return nav_bar, update_cart_count

# NAVBAR PARA OTRAS VISTAS (por ejemplo, vistas de producto)
def create_navbar_product(page):
    """
    Devuelve:
      1) Un AppBar con 'leading' que lleva a /home
      2) Un icono de carrito con contador
      3) Una función update_cart_count() para refrescar en 2do plano
    """

    cart_count = ft.Text(
        value="0",
        color="white",
        size=12,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    async def fetch_cart_count():
      items = await get_items(page)
      cart_count.value = str(len(items["cart"])) if items and "cart" in items else "0"
      try:
          cart_count.update()
      except AssertionError:
          # Ya no está en el árbol, ignoramos
          pass


    def update_cart_count():
        page.run_task(fetch_cart_count)

    cart_icon = ft.Container(
        content=ft.Stack(
            [
                fl.Lottie(
                    src="https://creativeferrets.com/assets/lottie/cart.json",
                    animate=True,
                    width=30,
                    height=30,
                ),
                ft.Container(
                    content=cart_count,
                    bgcolor="red",
                    border_radius=ft.border_radius.all(12),
                    alignment=ft.alignment.center,
                    width=20,
                    height=20,
                    offset=ft.Offset(0.8, -0.6),
                ),
            ]
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.only(right=20),
        on_click=lambda e: page.go("/cart"),
    )

    nav_bar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: page.go("/home"),
        ),
        bgcolor=ft.Colors.WHITE,
        actions=[cart_icon],
        elevation=0,
        elevation_on_scroll=0,
    )
    return nav_bar, update_cart_count

# FOOTER DE NAVEGACIÓN
def create_footer(page):
    """
    Un CupertinoNavigationBar que alterna entre /home, /user, /favorites, /contacto
    según el índice seleccionado.
    """
    return ft.CupertinoNavigationBar(
        on_change=lambda e: page.go(
            get_route_from_index(page, e.control.selected_index)
        ),
        selected_index=get_footer_selected_index(page.route),
        active_color=ft.Colors.BLACK,
        inactive_color=ft.Colors.BLACK54,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                selected_icon=ft.Icons.HOME_OUTLINED,
                bgcolor="#E62514",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOY,
                selected_icon=ft.Icons.BOY,
                bgcolor="#E62514",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.FAVORITE,
                selected_icon=ft.Icons.FAVORITE,
                bgcolor="#E62514",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SHOPPING_CART_OUTLINED,
                selected_icon=ft.Icons.SHOPPING_CART_OUTLINED,
                bgcolor="#E62514",
            ),
        ]
    )
