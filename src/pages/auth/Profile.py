from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.controls.Fecha import DatePickerField
from pages.utils.controls.inputs import MyInputField, MyDropdownField
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
        snack_bar = ft.SnackBar(ft.Text("Error al cargar los datos del usuario."), bgcolor=ft.Colors.RED)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    if not user_data:
        snack_bar = ft.SnackBar(ft.Text("No se encontraron datos del usuario."), bgcolor=ft.Colors.RED)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

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
        snack_bar = ft.SnackBar(ft.Text("No se encontraron datos del usuario."), bgcolor=ft.Colors.RED)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    

    name_field = MyInputField(label="Nombres", value=full_user_data.get("first_name", ""))
    last_name_field = MyInputField(label="Apellidos", value=full_user_data.get("last_name", ""))
    document_field = MyInputField(label="Número de Identificación", value=full_user_data.get("document", ""))
    email_field = MyInputField(label="E-mail", value=full_user_data.get("email", ""))
    phone_field = MyInputField(label="Celular", value=full_user_data.get("phone", ""))
    register_number_field = MyInputField(label="Número de Registro Civil", value=full_user_data.get("register_number", ""))
    city_field = MyInputField(label="Ciudad expedición", value=full_user_data.get("city", ""))
    department_field = MyInputField(label="Departamento", value=full_user_data.get("department", ""))
    notary_field = MyInputField(label="Notaría, Número o Registraduría", value=full_user_data.get("notaria_registraduria", ""))
    address_field = MyInputField(label="Dirección", value=full_user_data.get("direccion", ""))
    city_residence_field = MyInputField(label="Ciudad", value=full_user_data.get("ciudad", ""))
    state_field = MyInputField(label="Estado/Provincia", value=full_user_data.get("estado_provincia", ""))
    zip_field = MyInputField(label="Código Postal", value=full_user_data.get("zip", ""))
    country_field = MyDropdownField(label="País", options=["Colombia", "Ecuador", "Perú", "Otro"])


    def on_date_change(e):
        selected_date = e.control.value.strftime("%Y-%m-%d")
        birth_date_field.value = selected_date
        page.update()

    birth_date_field = DatePickerField(
        name="Fecha de Nacimiento",
        on_change=lambda date: print(f"Fecha seleccionada: {date}"),
    )
    birth_date_field.text_field.value = full_user_data.get("birth_date", "")
    
    def handle_save_click(e):
        updated_data = {
            "first_name": name_field.controls[1].value,
            "last_name": last_name_field.controls[1].value,
            "document_number": document_field.controls[1].value,
            "email": email_field.controls[1].value,
            "phone_number": phone_field.controls[1].value, 
            "birth_date": birth_date_field.value,
            "address": address_field.controls[1].value,
            "city": city_residence_field.controls[1].value,
            "state_province": state_field.controls[1].value,
            "zip_code": zip_field.controls[1].value,
            "country": country_field.controls[1].value,
            "civil_register_number": register_number_field.controls[1].value,
            "expedition_city": city_field.controls[1].value,
            "department": department_field.controls[1].value,
            "notary_registry": notary_field.controls[1].value,
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
            snack_bar = ft.SnackBar(ft.Text("Datos actualizados correctamente."), bgcolor=ft.Colors.GREEN)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
        except requests.RequestException as ex:
            snack_bar = ft.SnackBar(ft.Text("Error al actualizar los datos."), bgcolor=ft.Colors.RED)
            page.overlay.append(snack_bar)
            snack_bar.open = True
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
                                birth_date_field,
                                ft.Container(height=5),
                                ft.Text("Ubicacion", text_align="left", size=20, weight="bold"),
                                address_field,
                                city_residence_field,
                                state_field,
                                zip_field,
                                ft.Container(height=5),
                                ft.Text("Para más DocuFlow", text_align="left", size=20, weight="bold"),
                                register_number_field,
                                city_field,
                                department_field,
                                notary_field,
                                ft.Container(height=5),
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
