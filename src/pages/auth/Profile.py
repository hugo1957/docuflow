import flet as ft

from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.controls.Fecha import DatePickerField
from pages.utils.controls.inputs import MyInputField
from pages.utils.controls.dropdownFlag import CountryDropdown
from pages.endpoints.Auth import fetch_user_data, update_user_data, load_user
from pages.utils.state import departamentos_data


API_URL = "http://localhost:8000"


def ViewProfile(page):
    # Limpieza y configuración básica de la vista
    page.controls.clear()
    navbar, _ = create_navbar_product(page)
    page.appbar = navbar
    page.navigation_bar = create_footer(page)
    page.update()

    # Contenedor principal donde se pintará la UI
    main_container = ft.Container(expand=True)

    # ------------------------------------------------------------
    # FUNCIÓN ASÍNCRONA DE INICIALIZACIÓN (carga de datos y build de UI)
    # ------------------------------------------------------------
    async def init_view_async():
        # 1) Obtenemos user_data de client_storage (modo asíncrono)
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

        if not user_data or "id" not in user_data:
            sb = ft.SnackBar(
                ft.Text("No se encontraron datos del usuario."), bgcolor=ft.Colors.RED
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        user_id = user_data["id"]

        # 2) Llamamos al endpoint fetch_user_data
        try:
            full_user_data = await fetch_user_data(page, user_id)
        except Exception as ex:
            full_user_data = None
            print("Error al obtener datos del usuario:", ex)

        if not full_user_data:
            sb = ft.SnackBar(
                ft.Text("No se encontraron datos del usuario."), bgcolor=ft.Colors.RED
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        # 3) Construimos la UI con esos datos
        ui_container = build_profile_ui(page, user_id, user_data, full_user_data)
        main_container.content = ui_container
        page.update()

    # ------------------------------------------------------------
    # LANZAMOS init_view_async() EN SEGUNDO PLANO
    # ------------------------------------------------------------
    def init_view():
        page.run_task(init_view_async)

    init_view()

    # Retornamos main_container para pintarse inmediatamente
    return main_container

# ------------------------------------------------------------
# FUNCIÓN QUE CONSTRUYE TODOS LOS CAMPOS DE PERFIL (SINCRÓNICA)
# ------------------------------------------------------------
def build_profile_ui(page, user_id, user_data, full_user_data):
  profile_data = full_user_data.get("profile", {})
  print("Datos de usuario:", profile_data)
  # ====== Definición de campos ======
  name_field = MyInputField(
    label="Nombres",
    value=profile_data.get("first_name", "")
  )
  last_name_field = MyInputField(
    label="Apellidos",
    value=profile_data.get("last_name", "")
  )
  document_field = MyInputField(
    label="Número de Identificación",
    value=profile_data.get("document_number", "")
  )
  email_field = MyInputField(
    label="E-mail",
    value=profile_data.get("email", "")
  )
  phone_field = MyInputField(
    label="Celular",
    value=profile_data.get("phone_number", "")
  )

  birth_date_field = DatePickerField(
    name="Fecha de Nacimiento",
    on_change=lambda date: print(f"Fecha seleccionada: {date}"),
  )
  birth_date_field.text_field.value = profile_data.get("birth_date", "")

  address_field = MyInputField(
    label="Dirección",
    value=profile_data.get("address", "")
  )

  # ====== Departamentos y Ciudades ======
  departamentos = departamentos_data["departamentos"]

  def update_cities(e):
    selected_dept = department_dropdown.value
    city_dropdown.options = []
    for dept in departamentos:
      if dept["nombre"] == selected_dept:
        city_dropdown.options = [
          ft.dropdown.Option(ciudad) for ciudad in dept["ciudades"]
        ]
        city_dropdown.value = None
        e.page.update()
        break

  department_dropdown = ft.Dropdown(
    border_radius=ft.border_radius.all(15),
    content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
    bgcolor=ft.Colors.WHITE,
    border_color="#717171",
    label_style=ft.TextStyle(color="#717171"),
    border_width=0.5,
    options=[ft.dropdown.Option(dept["nombre"]) for dept in departamentos],
    on_change=update_cities,
  )
  city_dropdown = ft.Dropdown(
    border_radius=ft.border_radius.all(15),
    content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
    bgcolor=ft.Colors.WHITE,
    border_color="#717171",
    label_style=ft.TextStyle(color="#717171"),
    border_width=0.5,
    options=[],
  )

  preselected_dept = profile_data.get("department", "")
  preselected_city = profile_data.get("city", "")

  if preselected_dept:
    department_dropdown.value = preselected_dept
    for dept in departamentos:
      if dept["nombre"] == preselected_dept:
        city_dropdown.options = [
          ft.dropdown.Option(ciudad) for ciudad in dept["ciudades"]
        ]
        break
  if preselected_city:
    city_dropdown.value = preselected_city

  # ====== País (CountryDropdown) ======
  country_field = CountryDropdown()
  preselected_country = profile_data.get("country", "")
  if preselected_country:
    country_field.value = preselected_country

  # ====== Otros campos ======
  zip_field = MyInputField(
    label="Código Postal",
    value=profile_data.get("zip_code", "")
  )
  register_number_field = MyInputField(
    label="Número de Registro Civil",
    value=profile_data.get("civil_register_number", "")
  )
  city_field = MyInputField(
    label="Ciudad expedición",
    value=profile_data.get("expedition_city", "")
  )
  notary_field = MyInputField(
    label="Notaría, Número o Registraduría",
    value=profile_data.get("notary_registry", "")
  )

  # --------------------------------------------------------
  # on_click sincrónico -> llama a la corrutina handle_save
  # --------------------------------------------------------
  def handle_save_click(e):
    e.page.run_task(handle_save_click_async, e)

  # Corrutina que hace la lógica de guardar
  async def handle_save_click_async(e):
    updated_data = {
      "first_name": name_field.controls[1].value,
      "last_name": last_name_field.controls[1].value,
      "document_number": document_field.controls[1].value,
      "email": email_field.controls[1].value,
      "phone_number": phone_field.controls[1].value,
      "birth_date": birth_date_field.value,
      "address": address_field.controls[1].value,
      "department": department_dropdown.value,
      "city": city_dropdown.value,
      "zip_code": zip_field.controls[1].value,
      "country": country_field.value,
      "civil_register_number": register_number_field.controls[1].value,
      "expedition_city": city_field.controls[1].value,
      "notary_registry": notary_field.controls[1].value,
    }
    try:
      # Llamamos update_user_data (asíncrono)
      updated_user_data = await update_user_data(page, user_id, updated_data)
      if updated_user_data:
        # Volvemos a cargar la info
        await load_user(page)
        sb = ft.SnackBar(
          content=ft.Text("Datos de usuario actualizados."), 
          bgcolor=ft.Colors.GREEN
        )
        e.page.overlay.append(sb)
        sb.open = True
        e.page.update()
    except Exception as ex:
      sb = ft.SnackBar(
        content=ft.Text(f"Error actualizando datos: {ex}"), 
        bgcolor=ft.Colors.RED
      )
      e.page.overlay.append(sb)
      sb.open = True
      e.page.update()

  # --------------------------------------------------------
  # Construimos la UI final (Column, Container, etc.)
  # --------------------------------------------------------
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
                ft.Text(
                  "Mi Perfil",
                  text_align="left",
                  size=20,
                  weight="bold",
                ),
                ft.Container(height=5),
                name_field,
                last_name_field,
                document_field,
                email_field,
                phone_field,
                birth_date_field,
                ft.Container(height=5),
                ft.Text(
                  "Ubicación",
                  text_align="left",
                  size=20,
                  weight="bold",
                ),
                address_field,
                ft.Column(
                  spacing=0,
                  controls=[
                    ft.Text("País", style=ft.TextStyle(color="#717171")),
                    country_field,
                  ],
                ),
                ft.Column(
                  spacing=0,
                  controls=[
                    ft.Text("Departamento", style=ft.TextStyle(color="#717171")),
                    department_dropdown,
                  ],
                ),
                ft.Column(
                  spacing=0,
                  controls=[
                    ft.Text("Ciudad", style=ft.TextStyle(color="#717171")),
                    city_dropdown,
                  ],
                ),
                zip_field,
                ft.Container(height=5),
                ft.Text(
                  "Para más DocuFlow",
                  text_align="left",
                  size=20,
                  weight="bold",
                ),
                register_number_field,
                city_field,
                notary_field,
                ft.Container(height=5),
              ],
            ),
            ft.Container(
              alignment=ft.alignment.center,
              on_click=handle_save_click,  # Llama la función sincrónica
              ink=True,
              border_radius=ft.border_radius.all(35),
              width=350,
              height=40,
              bgcolor="#25D366",
              content=ft.Text(
                "Guardar",
                size=15,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
              ),
              padding=ft.padding.all(10),
            ),
          ],
        ),
      )
    ],
  )

  return container
