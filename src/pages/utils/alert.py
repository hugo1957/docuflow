import flet as ft


def show_construction_dialog(page, service_name, rol):
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Estamos trabajando en esto"),
        content=ft.Text(
            f"{rol} con {service_name} está en construcción. Por favor, inténtalo más tarde."),
        actions=[
            ft.TextButton(
                "Cerrar", on_click=lambda e: close_dialog(page, dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def close_dialog(page, dialog):
    dialog.open = False
    page.update()
