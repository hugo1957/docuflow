from pages.utils.dropdownFlag import CountryDropdown
from pages.utils.state import departamentos_data
from pages.utils.navigation import create_footer, create_navbar_product
from pages.utils.inputs import create_input_field, create_dropdown_field
import flet as ft
import re
import os
from pages.home import ViewHome
from pages.auth.Profile import ViewProfile
from pages.ProductDetail import ViewProductDetail
from pages.Cart import ViewCart
from pages.auth.PageNotFound import PageNotFound
from pages.PaymentSuccess import ViewPaymentSuccess
from pages.Checkout import ViewCheckout
from pages.auth.Login import ViewLogin
from pages.auth.Token import ViewToken
from pages.Favorites import ViewFavorites
from pages.Order import ViewOrders
from pages.OrderDetail import ViewOrderDetail
from pages.User import ViewUser
from pages.Domiciliario.RegisterDomi import ViewRegisterDomiciliario
from pages.InitPage import WelcomeView
# Extras
from pages.Extras.Terminos_condiciones import ViewTermsAndConditions
from pages.Extras.Politicas_privacidad import ViewPrivacyPolicy
from pages.Extras.Autorizacion_tratamiento_datos import ViewDataAuthorization
# Data
from pages.data.Registro_civil import ViewRegistroCivil


class ViewManager:
    def __init__(self, page):
        self.page = page
        self.view_cache = {}

    def get_view(self, route, params=None):
        if route in self.view_cache:
            return self.view_cache[route]

        if route == "/":
            view = ViewRegistroMenores
        elif route == "/phone-login":
            view = ViewLogin
        elif route == "/token":
            view = ViewToken
        elif route == "/home":
            view = ViewHome
        elif route == "/user":
            view = ViewUser
        elif route == "/profile":
            view = ViewProfile
        elif re.match(r"^/product-detail/.+", route):
            def view(page): return ViewProductDetail(
                page, params.get("product_url"))
        elif route == "/favorites":
            view = ViewFavorites
        elif route == "/cart":
            view = ViewCart
        elif route == "/checkout":
            view = ViewCheckout
        elif route == "/payment-success":
            view = ViewPaymentSuccess
        elif route == "/orders":
            view = ViewOrders
        elif re.match(r"^/order-detail/.+", route):
            def view(page): return ViewOrderDetail(
                page, params.get("order_id"))
        elif route == "/register-domiciliario":
            view = ViewRegisterDomiciliario
        # Data
        elif route == "/registro-civil":
            view = ViewRegistroCivil
        elif route == "/salida-menores":
            view = ViewRegistroMenores
        # Extras
        elif route == "/terms":
            view = ViewTermsAndConditions
        elif route == "/privacy-policy":
            view = ViewPrivacyPolicy
        elif route == "/data-authorization":
            view = ViewDataAuthorization
        else:
            view = PageNotFound

        self.view_cache[route] = view
        return view


def configure_page(page: ft.Page):
    page.adaptive = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.padding = ft.padding.all(0)

    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.window.always_on_top = True

    def handle_app_event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)

    page.on_app_lifecycle_state_change = handle_app_event


def handle_navigation(page, view_manager, route):
    params = {}
    if re.match(r"^/product-detail/.+", route):
        params["product_url"] = route[len("/product-detail/"):]
    elif re.match(r"^/order-detail/.+", route):
        params["order_id"] = route[len("/order-detail/"):]

    view_cls = view_manager.get_view(route, params)

    page.controls.clear()
    page.appbar = None
    page.navigation_bar = None

    view = view_cls(page)
    page.add(ft.SafeArea(content=view, expand=True))
    page.update()


async def main(page: ft.Page):
    configure_page(page)
    view_manager = ViewManager(page)

    def on_route_change(e):
        handle_navigation(page, view_manager, e.route)

    def on_view_pop(e):
        if page.controls:
            page.controls.pop()
            page.update()

    page.on_route_change = on_route_change
    page.on_view_pop = on_view_pop

    handle_navigation(page, view_manager, page.route)


def on_country_selected(country_name):
    print(f"Selected country: {country_name}")


def ViewRegistroMenores(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)

    # Campos principales del menor
    name_field = create_input_field("Nombres y Apellidos del Menor")
    document_field = create_input_field("Número de Identificación del Menor")
    birth_certificate_field = create_input_field(
        "Registro Civil de Nacimiento")
    passport_field = create_input_field("Número de Pasaporte (si aplica)")
    destination_field = CountryDropdown(on_country_change=on_country_selected)
    purpose_field = create_input_field("Propósito del Viaje")
    dates_field = create_input_field("Fechas de Salida y Regreso (AAAA-MM-DD)")
    birth_date_field = create_input_field(
        "Fecha de Nacimiento del Menor (AAAA-MM-DD)")

    # Información del padre
    father_name_field = create_input_field("Nombre del Padre")
    father_id_field = create_input_field("Número de Identificación del Padre")
    father_phone_field = create_input_field("Teléfono del Padre")
    father_death_certificate_field = create_input_field(
        "Registro Civil de Defunción (si fallecido)")
    is_father_deceased = ft.Checkbox(
        label="¿Padre fallecido?", on_change=lambda e: toggle_field_visibility(e, "father"))

    # Información de la madre
    mother_name_field = create_input_field("Nombre de la Madre")
    mother_id_field = create_input_field(
        "Número de Identificación de la Madre")
    mother_phone_field = create_input_field("Teléfono de la Madre")
    mother_death_certificate_field = create_input_field(
        "Registro Civil de Defunción (si fallecida)")
    is_mother_deceased = ft.Checkbox(
        label="¿Madre fallecida?", on_change=lambda e: toggle_field_visibility(e, "mother"))

    # Autorización escrita y casos especiales
    authorization_written = create_input_field(
        "Autorización Escrita del Padre/Madre (si aplica)")
    patria_potestad = create_input_field(
        "Sentencia Judicial de Patria Potestad (si aplica)")
    special_case_checkbox = ft.Checkbox(
        label="¿Aplica caso especial?", on_change=lambda e: toggle_field_visibility(e, "special_case"))

    # Dropdowns para departamento y ciudad
    departamentos = departamentos_data["departamentos"]
    department_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(dept["nombre"]) for dept in departamentos],
        on_change=lambda e: update_cities(e),
    )
    city_dropdown = ft.Dropdown(options=[])

    def update_cities(e):
        selected_department = e.control.value
        for dept in departamentos:
            if dept["nombre"] == selected_department:
                city_dropdown.options = [ft.dropdown.Option(
                    city) for city in dept["ciudades"]]
                city_dropdown.value = None
                page.update()
                break

    def toggle_field_visibility(e, field_type):
        if field_type == "father":
            father_death_certificate_field.disabled = not e.control.value
        elif field_type == "mother":
            mother_death_certificate_field.disabled = not e.control.value
        elif field_type == "special_case":
            patria_potestad.disabled = not e.control.value
        page.update()

    def validate_and_confirm(e):
        errors = []
        # Validar campos obligatorios
        required_fields = [
            (name_field, "Nombres y Apellidos del Menor"),
            (document_field, "Número de Identificación del Menor"),
            (birth_certificate_field, "Registro Civil de Nacimiento"),
            (destination_field, "Lugar de Destino del Viaje"),
            (purpose_field, "Propósito del Viaje"),
            (dates_field, "Fechas de Salida y Regreso"),
        ]
        for field, name in required_fields:
            if not field.controls[1].value.strip():
                errors.append(f"El campo '{name}' es obligatorio.")

        if is_father_deceased.value and not father_death_certificate_field.controls[1].value.strip():
            errors.append(
                "Debe proporcionar el 'Registro Civil de Defunción del Padre' si ha fallecido.")
        if is_mother_deceased.value and not mother_death_certificate_field.controls[1].value.strip():
            errors.append(
                "Debe proporcionar el 'Registro Civil de Defunción de la Madre' si ha fallecido.")
        if special_case_checkbox.value and not patria_potestad.controls[1].value.strip():
            errors.append(
                "Debe proporcionar la sentencia judicial de patria potestad si aplica un caso especial.")
        if not department_dropdown.value:
            errors.append("Debe seleccionar un Departamento.")
        if not city_dropdown.value:
            errors.append("Debe seleccionar una Ciudad.")

        if errors:
            dlg = ft.AlertDialog(
                title=ft.Text("Errores de Validación"),
                content=ft.Text("\n".join(errors)),
            )
            dlg.open = True
            page.overlay.append(dlg)
            page.update()
        else:
            show_confirmation_dialog()

    def show_confirmation_dialog():
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Guardado"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Nombres del Menor: {
                            name_field.controls[1].value}"),
                    # Mostrar otros campos relevantes
                ],
                spacing=10,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar", on_click=lambda _: close_dialog(dlg)),
                ft.TextButton("Confirmar", on_click=lambda _: save_data(dlg)),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def save_data(dlg):
        dlg.open = False
        page.go("/solicitud_guardada")

    def close_dialog(dlg):
        dlg.open = False
        page.update()

    save_button = ft.Container(
        alignment=ft.alignment.center,
        on_click=validate_and_confirm,
        ink=True,
        border_radius=ft.border_radius.all(35),
        width=350,
        height=40,
        bgcolor="#25D366",
        content=ft.Text("Guardar Solicitud", size=15,
                        color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        padding=ft.padding.all(10),
    )

    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Text("Registro de Permiso de Salida",
                    size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    scroll=ft.ScrollMode.HIDDEN,
                    controls=[
                        name_field,
                        document_field,
                        birth_certificate_field,
                        passport_field,
                        ft.Column(
                            controls=[
                                ft.Text("Lugar de Destino del Viaje",
                                        style=ft.TextStyle(color="#717171")),
                                destination_field,
                            ]
                        ),
                        purpose_field,
                        dates_field,
                        is_father_deceased,
                        father_name_field,
                        father_id_field,
                        father_phone_field,
                        father_death_certificate_field,
                        is_mother_deceased,
                        mother_name_field,
                        mother_id_field,
                        mother_phone_field,
                        mother_death_certificate_field,
                        special_case_checkbox,
                        authorization_written,
                        patria_potestad,
                        ft.Text("Departamento de Residencia del menor"),
                        department_dropdown,
                        ft.Text("Ciudad de Residencia del menor"),
                        city_dropdown,
                        save_button,
                    ],
                ),
            ),
        ],
    )
    return container


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
