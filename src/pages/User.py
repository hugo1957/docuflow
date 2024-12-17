
from pages.utils.navigation import create_navbar_product, create_footer
from functools import partial
import flet as ft
from pages.endpoints.Auth import logout_user

def ViewUser(page):
  page.controls.clear()
  page.appbar = create_navbar_product(page)[0]
  page.navigation_bar = create_footer(page)
  page.update()

  # Encabezado
  greeting_section = ft.Container(
    padding=ft.padding.symmetric(vertical=30, horizontal=20),
    content=ft.Column(
      [
        ft.Text("Hola,", size=18, color=ft.colors.BLUE_GREY_500),
        ft.Text("Hugo Puche", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
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
        ft.TextButton("Cancelar", on_click=lambda _: close_dialog(dlg)),
        ft.TextButton("Cerrar sesión", on_click=lambda _: confirm_logout(dlg), style=ft.ButtonStyle(color=ft.colors.RED_500)),
      ],
    )
    page.dialog = dlg
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
    {"icon": ft.Icons.ACCOUNT_BOX_OUTLINED, "label": "Perfil", "url": "/profile"},
    {"icon": ft.Icons.DELIVERY_DINING_OUTLINED, "label": "Pedidos", "url": "/orders"},
    {"icon": ft.Icons.PAYMENT_ROUNDED, "label": "Pagos", "url": "/payment-methods"},
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
                ft.Icon(action["icon"], size=28, color="#FF5700"),
                ft.Text(action["label"], size=10, text_align=ft.TextAlign.CENTER, color=ft.colors.BLUE_GREY_700),
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
    {"icon": ft.Icons.NOTIFICATIONS_NONE, "label": "Notificaciones", "url": "/notifications"},
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
    {"icon": ft.Icons.INFO_OUTLINE, "label": "Términos y Condiciones", "url": "/terms"},
    {"icon": ft.Icons.SECURITY, "label": "Política de Privacidad", "url": "/privacy-policy"},
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

  # Botón de cierre de sesión minimalista
  logout_section = ft.Container(
    padding=ft.padding.symmetric(vertical=20),
    alignment=ft.alignment.center,
    content=ft.TextButton(
      "Cerrar sesión",
      icon=ft.icons.LOGOUT,
      on_click=show_logout_dialog,
      style=ft.ButtonStyle(color=ft.colors.RED_500),
    ),
  )

  # Layout principal
  container = ft.Container(
    padding=ft.padding.symmetric(horizontal=10),
    alignment=ft.alignment.center,
    content=ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      
      controls=[
        greeting_section,
        ft.Text("Acciones Rápidas", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY_500),
        quick_actions_section,
        ft.Divider(),
        ft.Text("Configuración de Cuenta", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY_500),
        account_section,
        ft.Text("Más Opciones", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY_500),
        menu_section,
        logout_section,
      ],
      spacing=20,
      scroll=ft.ScrollMode.AUTO,
    ),
  )

  return container