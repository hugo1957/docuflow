from pages.utils.navigation import create_navbar_product, create_footer
from functools import partial
import flet as ft

def ViewUser(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)
    page.update()

    greeting_section = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            [
                ft.Text("Hola,", size=20),
                ft.Text("Hugo Puche", size=24, weight=ft.FontWeight.BOLD),
            ],
            spacing=10,
        ),
    )

    def navigate_to_url(e, url):
        page.go(url)

    def show_logout_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("¿Estás seguro de que deseas cerrar sesión?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: close_dialog(dlg)),
                ft.TextButton("Cerrar sesión", on_click=lambda _: confirm_logout(dlg)),
            ],
        )
        if page.overlay:  # Verifica si hay elementos en el overlay antes de eliminarlos
            page.overlay.pop()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def confirm_logout(dlg):
        close_dialog(dlg)  # Cierra el diálogo
        page.go("/")  # Redirige al inicio
        page.update()

    def close_dialog(dlg):
        dlg.open = False
        page.update()

    quick_actions = [
        {"icon": ft.Icons.PERSON, "label": "Datos de Perfil", "url": "/profile"},
        {"icon": ft.Icons.HEADSET, "label": "Centro de ayuda", "url": "/help"},
        {"icon": ft.Icons.HISTORY, "label": "Historial de pedidos", "url": "/orders"},
        {"icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "label": "Métodos de pago", "url": "/payment-methods"},
    ]

    quick_actions_controls = [
        ft.Container(
            padding=ft.padding.all(10),
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=8,
            width=80,
            height=80,
            on_click=partial(navigate_to_url, url=action["url"]),
            ink=True,
            content=ft.Column(
                [
                    ft.Icon(action["icon"], size=30),
                    ft.Text(action["label"], size=10, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
        )
        for action in quick_actions
    ]

    quick_actions_section = ft.Container(
        content=ft.Row(
            quick_actions_controls,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=ft.padding.all(10),
    )

    account_options = [
        {"icon": ft.Icons.ABC_OUTLINED, "label": "DocuFlow Pro", "url": "/docuflow-pro"},
        {"icon": ft.Icons.PLACE, "label": "Direcciones", "url": "/addresses"},
        {"icon": ft.Icons.LANGUAGE, "label": "Idioma", "url": "/language"},
        {"icon": ft.Icons.NOTIFICATIONS, "label": "Notificaciones", "url": "/notifications"},
    ]

    account_controls = [
        ft.Container(
            on_click=partial(navigate_to_url, url=option["url"]),
            ink=True,
            content=ft.ListTile(
                leading=ft.Icon(option["icon"]),
                title=ft.Text(option["label"]),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
            ),
        )
        for option in account_options
    ]

    account_section = ft.Column(account_controls, spacing=10)

    menu_items = [
        {"icon": ft.Icons.EDIT, "label": "Cambiar icono de DocuFlow", "url": "/change-icon"},
        {"icon": ft.Icons.STORE, "label": "Quiero ser un aliado estrategico de DocuFlow", "url": "/register-domiciliario"},
        {"icon": ft.Icons.INFO, "label": "Términos y Condiciones", "url": "/terms"},
        {"icon": ft.Icons.SECURITY, "label": "Política de Privacidad", "url": "/privacy-policy"},
        {"icon": ft.Icons.PERM_CONTACT_CAL, "label": "Autorización de tratamiento de datos personales", "url": "/data-authorization"},
    ]

    menu_controls = [
        ft.Container(
            on_click=partial(navigate_to_url, url=item["url"]),
            ink=True,
            content=ft.ListTile(
                leading=ft.Icon(item["icon"]),
                title=ft.Text(item["label"]),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
            ),
        )
        for item in menu_items
    ]

    menu_section = ft.Column(menu_controls, spacing=10)

    footer_section = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            [
                ft.TextButton("Cerrar sesión", on_click=show_logout_dialog),
                ft.Text(
                    "Versión 0.0.1 \nDocuFlow App\nBarranquilla, Atlántico\nsoporte@docuflow.com",
                    size=12,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    
    container = ft.Container(
        padding=ft.padding.all(10),
        content=ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                greeting_section,
                quick_actions_section,
                ft.Divider(height=1, thickness=1),
                account_section,
                menu_section,
                footer_section,
            ],
            spacing=10,
        ),
    )

    return container
