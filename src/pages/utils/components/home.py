import flet as ft
from pages.utils.image import create_image_with_loader
import flet_lottie as fl
API_URL = "http://localhost:8000"
def create_content(page, image, name, valor, product_id):
    if not image:
        image = "/assets/images/no-image.jpg"

    return ft.Container(
        width=200,
        height=350,
        expand=True,
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.Colors.GREY_100,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(width=10, height=10),
                                ft.IconButton(
                                    icon=ft.Icons.SHOPPING_CART_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    bgcolor="#FF5700",
                                    on_click=lambda _: page.go(
                                        f"/product-detail/{product_id}"
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            width=150,
                            height=200,
                            border_radius=ft.BorderRadius(
                                top_left=75,
                                top_right=75,
                                bottom_left=40,
                                bottom_right=40,
                            ),
                            bgcolor="#f0f0f0",
                            shadow=ft.BoxShadow(
                                blur_radius=15,
                                spread_radius=5,
                                color="rgba(0,0,0,0.2)",
                            ),
                            content=create_image_with_loader(
                                src=f"{API_URL}{image}",
                                width=150,
                                height=200,
                                fit=ft.ImageFit.FILL,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                ft.Text(
                    name,
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text(
                    f"${valor}",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=0,
        ),
    )

def create_products_grid(page, products_list):
    rows = []
    for i in range(0, len(products_list), 2):
        row_controls = []
        for product in products_list[i: i + 2]:
            row_controls.append(
                ft.Container(
                    width="calc(50% - 10px)",
                    content=create_content(
                        page,
                        product["photo"],
                        product["name"],
                        product["price"],
                        product["id"],
                    ),
                )
            )
        rows.append(
            ft.Row(scroll=ft.ScrollMode.AUTO,
                   spacing=10, controls=row_controls)
        )
    return ft.Container(
        padding=ft.padding.all(5),
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=rows,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

def menu(page):
  container = ft.PopupMenuButton(
        icon=ft.Icons.FILTER_LIST_ALT,
        icon_color=ft.Colors.WHITE,
        elevation=0,
        menu_position=ft.PopupMenuPosition.OVER,
        shadow_color=ft.Colors.BLACK,
        tooltip="Filtros",
        items=[
            ft.PopupMenuItem(
                content=ft.Row(
                    controls=[
                        ft.Text("Ascendente", size=15),
                        ft.Icon(ft.Icons.ARROW_UPWARD,
                                size=20, color="#FF5700"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    controls=[
                        ft.Text("Descendente", size=15),
                        ft.Icon(ft.Icons.ARROW_DOWNWARD,
                                size=20, color="#FF5700"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    controls=[
                        ft.Text("Más Ventas", size=15),
                        ft.Icon(ft.Icons.SELL, size=20, color="#FF5700"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
        ],
    )

  return container

def redes(page):
  container = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Redes Sociales", size=15, weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=fl.Lottie(
                            src="https://creativeferrets.com/assets/lottie/facebook.json",
                            reverse=False,
                            animate=True,
                        ),
                        width=40,
                        height=40,
                    ),
                    ft.VerticalDivider(thickness=3),
                    ft.Container(
                        content=fl.Lottie(
                            src="https://creativeferrets.com/assets/lottie/instagram.json",
                            reverse=False,
                            animate=True,
                        ),
                        width=40,
                        height=40,
                    ),
                    ft.VerticalDivider(thickness=3),
                    ft.Container(
                        content=fl.Lottie(
                            src="https://creativeferrets.com/assets/lottie/youtube.json",
                            reverse=False,
                            animate=True,
                        ),
                        width=40,
                        height=40,
                    ),
                ],
            ),
        ],
    )
  return container