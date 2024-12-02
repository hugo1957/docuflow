import flet as ft

def get_drawer_selected_index(route):
    route_to_index = {
        "/home": 0,
        "/inventario": 1,
        "/saldo-planta": 2,
    }
    return route_to_index.get(route, 0)


def get_footer_selected_index(route):
    route_to_index = {
        "/home": 0,
        "/inventario": 1,
        "/saldo-planta": 2,
    }
    return route_to_index.get(route, 0)


def get_route_from_index(page, index, footer=False):
    if not footer:
        page.close(page.drawer)

    drawer_routes = [
        "/home",
        "/inventario",
        "/saldo-planta",
    ]

    footer_routes = [
        "/home",
        "/inventario",
        "/saldo-planta",
    ]
    routes = footer_routes if footer else drawer_routes
    return routes[index] if index < len(routes) else "/home"


def create_navbar(page, drawer):
    
    return ft.AppBar(
        bgcolor=ft.colors.WHITE,
        elevation_on_scroll=0,
        leading=ft.IconButton(
            ft.icons.MENU, icon_size=30, on_click=lambda e: page.open(drawer), icon_color="#E62514"),
        title=ft.Image(src="logo-blanco.png", width=60, height=60),
        center_title=True,
        
    )


def create_appbar_init(page, request_permission):
    page.controls.clear()
    return ft.AppBar(
        bgcolor=ft.colors.WHITE,
        elevation_on_scroll=0,
        elevation=0,
        actions=[
            ft.IconButton(
                ft.icons.NOTIFICATIONS,
                icon_size=30,
                icon_color="#E62514",
                on_click=lambda _: request_permission(_)
            ),
            ft.Container(width=10),
        ],
    )


def create_appbar(page):
    is_login = page.route == "/login"
    is_forgot_password = page.route == "/forgot-password"
    button_back = "/login" if is_forgot_password else "/"

    return ft.AppBar(
        bgcolor=ft.colors.WHITE,
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK_OUTLINED,
            icon_size=20,
            on_click=lambda e: page.go(button_back),
            icon_color="#E62514",
        ),
        # title=ft.Text(
        #     title_text,
        #     size=15,
        #     color=ft.colors.WHITE,
        #     text_align="center",
        #     weight=ft.FontWeight.BOLD,
        #     font_family="Heavitas",
        # ),
        # actions=[
        #     ft.Container(
        #         content=ft.Text(
        #             button_text,
        #             size=13,
        #             color=ft.colors.WHITE,
        #             weight=ft.FontWeight.BOLD
        #         ),
        #         padding=ft.padding.symmetric(horizontal=15, vertical=8),
        #         border_radius=ft.border_radius.all(5),
        #         bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE),
        #         ink=True,
        #         on_click=lambda _: page.go(button_action),  # Cambia de login, registro o iniciar sesión
        #     ),
        #     ft.Container(width=10),  # Espaciador opcional
        # ],
        center_title=True,
        elevation_on_scroll=0,
        elevation=0,
    )


def create_footer(page):
    return ft.CupertinoNavigationBar(
        on_change=lambda e: page.go(get_route_from_index(
            page, e.control.selected_index, footer=True)),
        selected_index=get_footer_selected_index(page.route),
        active_color="#E62514",
        inactive_color="#AC1A17",
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.HOME,
                selected_icon=ft.icons.HOME_OUTLINED,
                bgcolor="#E62514",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.CARD_GIFTCARD,
                selected_icon=ft.icons.CARD_GIFTCARD_OUTLINED,
                bgcolor="#E62514",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.WORK,
                selected_icon=ft.icons.WORK_OUTLINED,
                bgcolor="#E62514",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.CONTACT_PAGE,
                selected_icon=ft.icons.CONTACT_PAGE_OUTLINED,
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
                            color=ft.colors.TRANSPARENT,),
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
                            icon=ft.icons.CLOSE,
                            on_click=lambda e: page.close(page.drawer),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                ),
            ),
            ft.Divider(thickness=3),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.HOME),
                label="Inicio",
                selected_icon=ft.icons.HOME_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.INVENTORY),
                label="Inventario P03",
                selected_icon=ft.icons.INVENTORY_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.INVENTORY_2),
                label="Saldo Planta P03",
                selected_icon=ft.icons.INVENTORY_2_OUTLINED,
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


def pagination(page, update_table, page_number, search_term):
    def next_page(e):
        nonlocal page_number
        page_number += 1
        update_table(page_number, search_term)

    def previous_page(e):
        nonlocal page_number
        if page_number > 1:
            page_number -= 1
        update_table(page_number, search_term)

    return ft.Row(
        controls=[
            ft.ElevatedButton(text="Anterior", on_click=previous_page, style=ft.ButtonStyle(
                color="#E62514", elevation=2)),
            ft.Container(),
            ft.ElevatedButton(text="Siguiente", on_click=next_page, style=ft.ButtonStyle(
                color="#E62514", elevation=2))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
