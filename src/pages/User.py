import flet as ft
from functools import partial
from pages.utils.navigation import create_navbar_product, create_footer
from pages.endpoints.Auth import logout_user
from pages.endpoints.User import validate_user

def ViewUser(page: ft.Page):
    # Limpieza y configuración básica de la vista
    page.controls.clear()
    navbar, update_cart_count = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Contenedor principal donde se pintará la UI
    main_container = ft.Container(expand=True)

    # ------------------------------------------------------------
    # FUNCIÓN ASÍNCRONA DE INICIALIZACIÓN (carga de datos y build de UI)
    # ------------------------------------------------------------
    async def init_view_async():
        # 1) Validar usuario
        is_valid = await validate_user(page)
        if not is_valid:
            return  # Redirección ya realizada en validate_user

        # 2) Obtener user_data de client_storage
        try:
            user_data = await page.client_storage.get_async("creativeferrets.tienda.user")
        except Exception as ex:
            sb = ft.SnackBar(
                ft.Text(f"Error al cargar los datos del usuario: {ex}"), bgcolor=ft.Colors.RED
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        if not user_data:
            sb = ft.SnackBar(
                ft.Text("No se encontraron datos del usuario."), bgcolor=ft.Colors.RED
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        # 3) Construir la UI con esos datos
        ui_container = build_user_ui(page, user_data)
        main_container.content = ui_container
        page.update()

    # ------------------------------------------------------------
    # LANZAR init_view_async() EN SEGUNDO PLANO
    # ------------------------------------------------------------
    def init_view():
        page.run_task(init_view_async)

    init_view()

    # Retornar main_container para pintarse inmediatamente
    return main_container

# ------------------------------------------------------------
# FUNCIÓN QUE CONSTRUYE LA UI DE USUARIO (SINCRÓNICA)
# ------------------------------------------------------------
def build_user_ui(page: ft.Page, user_data: dict):
    # Definir secciones y controles
    greeting_section = ft.Container(
        padding=ft.padding.symmetric(vertical=30, horizontal=20),
        content=ft.Column(
            [
                ft.Text("Hola,", size=18, color=ft.Colors.BLUE_GREY_500),
                ft.Text(
                    f"{user_data['get_full_name']}",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Text(
                    "Por favor, modifica tu perfil para colocar tus datos.",
                    size=14,
                    color=ft.Colors.RED_500,
                ) if user_data.get('get_full_name') == "Usuario Nuevo" else ft.Container(),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=5,
        ),
    )

    # Navegación
    def navigate_to_url(e, url):
        page.go(url)

    def show_logout_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("¿Deseas cerrar sesión?"),
            actions=[
                ft.TextButton(
                    "Cancelar", on_click=lambda _: close_dialog(dlg)),
                ft.TextButton("Cerrar sesión", on_click=lambda _: confirm_logout(
                    dlg), style=ft.ButtonStyle(color=ft.Colors.RED_500)),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def confirm_logout(dlg):
        close_dialog(dlg)
        logout_user(page)

    def close_dialog(dlg):
        dlg.open = False
        page.update()

    # Acciones rápidas envueltas en Container con Card
    quick_actions = [
        {"icon": ft.Icons.ACCOUNT_BOX_OUTLINED,
            "label": "Perfil", "url": "/profile"},
        {"icon": ft.Icons.DELIVERY_DINING_OUTLINED,
         "label": "Pedidos", "url": "/orders"},
        {"icon": ft.Icons.PAYMENT_ROUNDED,
            "label": "Pagos", "url": "/payment-methods"},
        {"icon": ft.Icons.HELP_CENTER_OUTLINED, "label": "Ayuda", "url": "/help"},
    ]

    quick_actions_section = ft.Row(
        controls=[
            ft.Container(
                on_click=partial(navigate_to_url, url=action["url"]),
                content=ft.Card(
                    elevation=2,
                    content=ft.Container(
                        width=80,
                        height=80,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            [
                                ft.Icon(action["icon"], size=28,
                                        color="#FF5700"),
                                ft.Text(action["label"], size=10, text_align=ft.TextAlign.CENTER,
                                        color=ft.Colors.BLUE_GREY_700),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                ),
            )
            for action in quick_actions
        ],
        scroll=ft.ScrollMode.ALWAYS,
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        spacing=10,
    )

    # Opciones de cuenta
    account_options = [
        {"icon": ft.Icons.LANGUAGE, "label": "Idioma", "url": "/language"},
        {"icon": ft.Icons.NOTIFICATIONS_NONE,
         "label": "Notificaciones", "url": "/notifications"},
    ]

    account_section = ft.Column(
        [
            ft.Container(
                on_click=partial(navigate_to_url, url=option["url"]),
                ink=True,
                content=ft.ListTile(
                    leading=ft.Icon(option["icon"], color="#FF5700"),
                    title=ft.Text(option["label"]),
                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                ),
            )
            for option in account_options
        ],
        spacing=10,
    )

    # Menú adicional
    menu_items = [
        {"icon": ft.Icons.INFO_OUTLINE,
            "label": "Términos y Condiciones", "url": "/terms"},
        {"icon": ft.Icons.SECURITY, "label": "Política de Privacidad",
         "url": "/privacy-policy"},
    ]

    menu_section = ft.Column(
        [
            ft.Container(
                on_click=partial(navigate_to_url, url=item["url"]),
                ink=True,
                content=ft.ListTile(
                    leading=ft.Icon(item["icon"], color="#FF5700"),
                    title=ft.Text(item["label"]),
                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                ),
            )
            for item in menu_items
        ],
        spacing=10,
    )
    domiciliario_items = [
        {"icon": ft.Icons.DELIVERY_DINING_OUTLINED,
            "label": "Quiero Ser Domiciliario", "url": "/register-domiciliario"},
    ]
    domiciliario_section = ft.Column(
        [
            ft.Container(
                on_click=partial(navigate_to_url, url=item["url"]),
                ink=True,
                content=ft.ListTile(
                    leading=ft.Icon(item["icon"], color="#FF5700"),
                    title=ft.Text(item["label"]),
                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                ),
            )
            for item in domiciliario_items
        ],
        spacing=10,
    )

    # Botón de cierre de sesión minimalista
    logout_section = ft.Container(
        padding=ft.padding.symmetric(vertical=20),
        alignment=ft.alignment.center,
        content=ft.TextButton(
            "Cerrar sesión",
            icon=ft.Icons.LOGOUT,
            on_click=show_logout_dialog,
            style=ft.ButtonStyle(color=ft.Colors.RED_500),
        ),
    )

    # Layout principal
    container = ft.Container(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            greeting_section,
            ft.Text("Acciones Rápidas", size=14,
                    weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_500),
            quick_actions_section,
            ft.Divider(),
            ft.Text("Domiciliario", size=14, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_500),
            domiciliario_section,
            ft.Divider(),
            ft.Text("Configuración de Cuenta", size=14,
                    weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_500),
            account_section,
            ft.Text("Más Opciones", size=14, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_500),
            menu_section,
            logout_section,
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    ),
      padding=ft.padding.all(10)
    )

    return container
