import flet as ft
import asyncio
from pages.utils.navigation import create_footer, create_navbar_home
from pages.utils.carusel import create_carousel
from pages.endpoints.Auth import refresh_token
from pages.endpoints.Tienda import (
    fetch_and_cache_categories,
    fetch_and_cache_products,
    update_cache_in_background,
)
from pages.utils.components.home import create_products_grid, menu, redes
from pages.endpoints.User import validate_user
API_URL = "https://api.creativeferrets.com"

def ViewHome(page):
    # 1) LIMPIA Y CONFIGURA LA INTERFAZ CON TUS ESTILOS
    page.controls.clear()
    navbar, update_navbar = create_navbar_home(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    pb = menu(page)  # Menú lateral
    redes_sociales = redes(page)

    # Contenedor dinámico para productos, y Tabs vacías por ahora
    dynamic_content = ft.Container()
    tabs = ft.Tabs(
        selected_index=0,
        indicator_color="#FF5700",
        indicator_border_radius=ft.border_radius.all(10),
        scrollable=True,
        indicator_tab_size=False,
        overlay_color="transparent",
        tabs=[],  # se llenarán luego
    )

    # Estructura principal de la pantalla con tus estilos
    container = ft.Container(
        padding=ft.padding.all(0),
        alignment=ft.alignment.center,
        content=ft.Column(
            spacing=0,
            controls=[
                # Barra verde superior con buscador
                ft.Container(
                    bgcolor="#007354",
                    padding=ft.padding.all(10),
                    content=ft.Row(
                        controls=[
                            ft.TextField(
                                border_radius=ft.border_radius.all(10),
                                content_padding=ft.padding.symmetric(
                                    horizontal=20, vertical=15
                                ),
                                bgcolor=ft.Colors.WHITE,
                                border_color="#717171",
                                label_style=ft.TextStyle(color="#717171"),
                                border_width=0.5,
                                expand=True,
                                prefix_icon=ft.Icons.SEARCH,
                                hint_text="Buscar en docuflowapp.com",
                            ),
                            pb,
                        ]
                    ),
                ),
                # Columna que contendrá la UI principal
                ft.Column(
                    scroll=ft.ScrollMode.HIDDEN,
                    spacing=0,
                    expand=True,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            width="100%",
                            height=50,
                            padding=ft.padding.all(10),
                            on_click=lambda _: print("Clickable without Ink clicked!"),
                            ink=True,
                            content=ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SHARE_LOCATION_SHARP,
                                        color=ft.Colors.BLACK,
                                        size=20
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Enviar a Baranquilla",
                                            color=ft.Colors.BLACK
                                        )
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            alignment=ft.alignment.center,
                            content=create_carousel(page),
                            padding=ft.padding.all(10),
                        ),
                        tabs,
                        dynamic_content,
                        redes_sociales,
                    ],
                ),
            ],
        ),
    )

    update_navbar()

    # 2) DEFINIMOS UNA FUNCIÓN ASÍNCRONA PARA CARGAR DATOS
    async def init_home_data():
        """
        Carga token, usuario, categorías y productos de forma asíncrona,
        luego actualiza la UI.
        """
        is_valid = await validate_user(page)
        if not is_valid:
            return  # Redirección ya realizada en validate_user

        try:
            # 2.0 Refrescar token si es necesario
            await refresh_token(page)
        except Exception as e:
            print(f"Error refrescando token: {e}")
        # 2.1 Cargar categorías
        try:
            categories_data = await page.client_storage.get_async("creativeferrets.tienda.categories")
            if not categories_data:
                # Llamamos async:
                categories_data = await fetch_and_cache_categories(page)
            if not categories_data:
                categories_data = {"categories": []}
        except Exception as e:
            print(f"Error cargando categorías: {e}")
            categories_data = {"categories": []}

        # 2.2 Cargar productos
        try:
            result_products = await page.client_storage.get_async("creativeferrets.tienda.products")
            if not result_products:
                result_products = await fetch_and_cache_products(page)
            if not result_products:
                result_products = {"products": []}
        except Exception as e:
            print(f"Error cargando productos: {e}")
            result_products = {"products": []}

        all_products = result_products["products"]
        categories_list = categories_data["categories"]

        # 2.3 Construimos las pestañas con tus estilos
        new_tabs = []
        for cat in categories_list:
            tab_name = cat["name"]
            new_tabs.append(
                ft.Tab(
                    tab_content=ft.Container(
                        width=150,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    tab_name,
                                    size=15,
                                    color=ft.Colors.BLACK,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(5),
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(10),
                    )
                )
            )
        tabs.tabs = new_tabs

        # Funciones auxiliares para manejar tabs
        def update_tab_colors(selected_index):
            for i, tab in enumerate(tabs.tabs):
                container = tab.tab_content
                column = container.content
                text = column.controls[0]
                if i == selected_index:
                    container.bgcolor = "#FF5700"
                    text.color = ft.Colors.WHITE
                else:
                    container.bgcolor = None
                    text.color = ft.Colors.BLACK

        def create_tab_content(index):
            if index < len(categories_list):
                cat_name = categories_list[index]["name"]
                category_id = categories_list[index]["id"]
                filtered_products = [
                    p for p in all_products if p["category"] == category_id
                ]
                if filtered_products:
                    return ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    f"Todo sobre {cat_name}",
                                    size=20,
                                    weight=ft.FontWeight.BOLD
                                ),
                                create_products_grid(page, filtered_products),
                            ]
                        ),
                        padding=ft.padding.all(10),
                    )
                else:
                    return ft.Container(
                        content=ft.Text("No hay productos disponibles en esta sección"),
                        padding=ft.padding.all(10),
                    )
            return ft.Container(content=ft.Text("No hay productos en esta categoría."))

        def on_tab_change(e):
            selected_index = e.control.selected_index
            update_tab_colors(selected_index)
            dynamic_content.content = create_tab_content(selected_index)
            page.update()

        tabs.on_change = on_tab_change

        # Pinta la primera pestaña si hay categorías
        if new_tabs:
            dynamic_content.content = create_tab_content(0)
            update_tab_colors(0)

        # Actualiza la interfaz final
        page.update()

        # 2.4 Actualizar caché en 2do plano (opcional)
        page.run_task(
            update_cache_in_background,
            page,
            "creativeferrets.tienda.categories",
            fetch_and_cache_categories,
        )
        page.run_task(
            update_cache_in_background,
            page,
            "creativeferrets.tienda.products",
            fetch_and_cache_products,
        )

    # 3) EJECUTAMOS LA FUNCIÓN ASÍNCRONA SIN BLOQUEAR
    page.run_task(init_home_data)

    # 4) RETORNAMOS EL CONTENEDOR CON TUS ESTILOS, PARA QUE SE MUESTRE DE INMEDIATO
    return container
