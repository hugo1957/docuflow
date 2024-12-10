import flet as ft

def get_drawer_selected_index(route):
    route_to_index = {
        "/home": 0,
        "/user": 1,
        "/favorites": 2,
        "/contacto": 3,
    }
    return route_to_index.get(route, 0)


def get_footer_selected_index(route):
    route_to_index = {
        "/home": 0,
        "/user": 1,
        "/favorites": 2,
        "/contacto": 3,
    }
    return route_to_index.get(route, 0)


def get_route_from_index(page, index, footer=False):
    if not footer:
        page.close(page.drawer)

    drawer_routes = [
        "/home",
        "/user",
        "/favorites",
        "/contacto",
    ]

    footer_routes = [
        "/home",
        "/user",
        "/favorites",
        "/contacto",
    ]
    routes = footer_routes if footer else drawer_routes
    return routes[index] if index < len(routes) else "/home"

def create_navbar_home(page):
    def update_cart_count():
        cart = page.session.get("cart")
        if cart is None:
            cart = []
        cart_count.value = str(len(cart))
        cart_count.update()

    cart = page.session.get("cart")
    if cart is None:
        cart = []

    cart_count = ft.Text(
        str(len(cart)),
        color="white",
        size=12,
        weight=ft.FontWeight.BOLD,
    )

    cart_icon = ft.Container(
        content=ft.Stack(
            [
                ft.Lottie(
                    src="https://creativeferrets.com/assets/lottie/cart.json",
                    animate=True,
                    width=30,
                    height=30,
                    
                    ),
                ft.Container(
                    content=cart_count,
                    bgcolor="red",
                    border_radius=ft.border_radius.all(12),
                    padding=ft.padding.all(0),
                    alignment=ft.alignment.center,
                    width=24,
                    height=24,
                    offset=ft.Offset(0.8, -0.6),
                ),
            ]
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.only(right=20),
        on_click=lambda e: page.go("/cart"),
    )

    nav_bar = ft.AppBar(
        title=ft.Text("DocuFlow", color="white"),
        bgcolor="#007354",
        actions=[cart_icon],
    )
    return nav_bar, update_cart_count

def create_navbar_product(page):
    def update_cart_count():
        cart = page.session.get("cart")
        if cart is None:
            cart = []
        cart_count.value = str(len(cart))
        cart_count.update()

    cart = page.session.get("cart")
    if cart is None:
        cart = []

    cart_count = ft.Text(
        str(len(cart)),
        color="white",
        size=12,
        weight=ft.FontWeight.BOLD,
    )

    cart_icon = ft.Container(
        content=ft.Stack(
            [
                ft.Lottie(
                    src="https://creativeferrets.com/assets/lottie/cart.json",
                    animate=True,
                    width=30,
                    height=30,
                    
                    ),
                ft.Container(
                    content=cart_count,
                    bgcolor="red",
                    border_radius=ft.border_radius.all(12),
                    padding=ft.padding.all(0),
                    alignment=ft.alignment.center,
                    width=24,
                    height=24,
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
            on_click=lambda e: page.go("/"),
        ),
        bgcolor=ft.Colors.WHITE,
        actions=[cart_icon],
    )
    return nav_bar, update_cart_count







def create_footer(page):
    return ft.CupertinoNavigationBar(
        on_change=lambda e: page.go(get_route_from_index(
            page, e.control.selected_index, footer=True)),
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


def create_drawer(page):
    page.controls.clear()
    page.update()

    return ft.NavigationDrawer(
        on_change=lambda e: page.go(
            get_route_from_index(page, e.control.selected_index)),
        selected_index=get_drawer_selected_index(page.route),
        indicator_color="#AC1A17",
        controls=[
            ft.Container(
                padding=ft.padding.all(5),
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            color=ft.Colors.TRANSPARENT,),
                        ft.Container(
                            content=ft.Image(
                                src="icon.png",
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            width=50,
                            height=50,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e: page.close(page.drawer),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                ),
            ),
            ft.Divider(thickness=3),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.Icons.HOME),
                label="Inicio",
                selected_icon=ft.Icons.HOME_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.Icons.INVENTORY),
                label="Inventario P03",
                selected_icon=ft.Icons.INVENTORY_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.Icons.INVENTORY_2),
                label="Saldo Planta P03",
                selected_icon=ft.Icons.INVENTORY_2_OUTLINED,
            ),
            ft.Container(
                height=page.window.height-300,
            ),
            ft.Divider(thickness=2),
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "© 2024 Empanorte", weight=ft.FontWeight.BOLD),
                        ft.Text("Todos los derechos reservados"),
                    ],
                    expand=True,
                    alignment=ft.alignment.center,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
            )
        ]
    )

