from pages.utils.inputs import create_input_field, create_dropdown_field
from pages.utils.alert import show_construction_dialog
from pages.utils.navigation import create_footer, create_navbar_product
import flet as ft
import datetime
import requests
API_URL = "http://localhost:8000"

def ViewProfile(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)
    
    try:
        user_data = page.client_storage.get("creativeferrets.tienda.user")
    except TimeoutError:
        return ft.SnackBar(ft.Text("Error al cargar los datos del usuario."), bgcolor=ft.Colors.RED)
    
    if not user_data:
        return ft.SnackBar(ft.Text("Error al cargar los datos del usuario."), bgcolor=ft.Colors.RED)

    user_id = user_data["id"]

    def fetch_user_data():
        try:
            access_token = page.client_storage.get("creativeferrets.tienda.access_token")
            response = requests.get(
                f"{API_URL}/api/user/user/{user_id}/",
                headers={
                    "Authorization": f"JWT {access_token}",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al cargar los datos del usuario: {e}")
            return None

    full_user_data = fetch_user_data()
    if not full_user_data:
        return ft.SnackBar(ft.Text("No se pudieron cargar los datos completos."), bgcolor=ft.Colors.RED)
    

    name_field = create_input_field("Nombres")
    name_field.controls[1].value = full_user_data.get("first_name", "")
    
    last_name_field = create_input_field("Apellidos")
    last_name_field.controls[1].value = full_user_data.get("last_name", "")
    
    document_field = create_input_field("Número de Identificación")
    document_field.controls[1].value = full_user_data.get("document", "")
    
    email_field = create_input_field("E-mail")
    email_field.controls[1].value = full_user_data.get("email", "")
    
    phone_field = create_input_field("Celular")
    phone_field.controls[1].value = full_user_data.get("phone", "")
    
    register_number_field = create_input_field("Número de Registro Civil")
    register_number_field.controls[1].value = full_user_data.get("register_number", "")
    
    city_field = create_input_field("Ciudad expedición")
    city_field.controls[1].value = full_user_data.get("city", "")
    
    deparment_field = create_input_field("Departamento")
    deparment_field.controls[1].value = full_user_data.get("department", "")
    
    notaria_registraduria = create_input_field("Notaría, Número o Registraduría")
    notaria_registraduria.controls[1].value = full_user_data.get("notaria_registraduria", "")
    
    direccion = create_input_field("Dirección")
    direccion.controls[1].value = full_user_data.get("direccion", "")
    
    ciudad = create_input_field("Ciudad")
    ciudad.controls[1].value = full_user_data.get("ciudad", "")
    
    estado_provincia = create_input_field("Estado/Provincia")
    estado_provincia.controls[1].value = full_user_data.get("estado_provincia", "")
    
    zip = create_input_field("Código Postal")
    zip.controls[1].value = full_user_data.get("zip", "")
    
    pais = create_dropdown_field("País", options=["Colombia", "Ecuador", "Perú", "Otro"])
    pais.controls[1].value = full_user_data.get("pais", "")

    def on_date_change(e):
        selected_date = e.control.value.strftime("%Y-%m-%d")
        birth_date_field.value = selected_date
        page.update()

    birth_date_field = ft.TextField(
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        value=full_user_data.get("birth_date", ""),
        expand=True,
    )

    def handle_save_click(e):
        updated_data = {
            "first_name": name_field.controls[1].value,
            "last_name": last_name_field.controls[1].value,
            "document_number": document_field.controls[1].value,
            "email": email_field.controls[1].value,
            "phone": phone_field.controls[1].value, 
            "birth_date": birth_date_field.value,
            "direccion": direccion.controls[1].value,
            "ciudad": ciudad.controls[1].value,
            "estado_provincia": estado_provincia.controls[1].value,
            "zip": zip.controls[1].value,
            "pais": pais.controls[1].value,
            "register_number": register_number_field.controls[1].value,
            "city": city_field.controls[1].value,
            "department": deparment_field.controls[1].value,
            "notaria_registraduria": notaria_registraduria.controls[1].value,
        }

        try:
            access_token = page.client_storage.get("creativeferrets.tienda.access_token")
            response = requests.put(
                f"{API_URL}/api/user/user/edit/{user_id}/",
                json=updated_data,
                headers={
                    "Authorization": f"JWT {access_token}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            page.snack_bar = ft.SnackBar(ft.Text("Datos actualizados exitosamente."), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open()
            page.update()
        except requests.RequestException as ex:
            page.snack_bar = ft.SnackBar(ft.Text("Error al actualizar los datos."), bgcolor=ft.Colors.RED)
            page.snack_bar.open()
            print(ex)
            page.update()

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.HIDDEN,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            spacing=5,
                            controls=[
                                ft.Container(height=5),
                                ft.Text("Mi Perfil", text_align="left", size=20, weight="bold"),
                                ft.Container(height=5),

                                name_field,
                                last_name_field,
                                document_field,
                                email_field,
                                phone_field,
                                ft.Column(
                                    controls=[
                                        ft.Text("Fecha de Nacimiento", style=ft.TextStyle(color="#717171")),
                                        ft.Row(
                                            controls=[
                                                birth_date_field,
                                                ft.IconButton(
                                                    icon=ft.Icons.CALENDAR_MONTH,
                                                    icon_color="blue",
                                                    on_click=lambda e: page.open(
                                                        ft.DatePicker(
                                                            first_date=datetime.datetime(year=2023, month=10, day=1),
                                                            last_date=datetime.datetime(year=2024, month=10, day=1),
                                                            on_change=on_date_change,
                                                        )
                                                    ),
                                                ),
                                            ],
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                    ],
                                    spacing=10,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                ),
                                ft.Container(height=5),
                                ft.Text("Ubicacion", text_align="left", size=20, weight="bold"),
                                direccion,
                                ciudad,
                                estado_provincia,
                                zip,
                                pais,
                                ft.Container(height=5),
                                ft.Text("Para más DocuFlow", text_align="left", size=20, weight="bold"),
                                register_number_field,
                                city_field,
                                deparment_field,
                                notaria_registraduria,
                            ]
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            on_click=handle_save_click,
                            ink=True,
                            border_radius=ft.border_radius.all(35),
                            width=350,
                            height=40,
                            bgcolor="#25D366",
                            content=ft.Text(
                                "Guardar", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),
                    ]
                )
            )
        ]
    )

    return container
