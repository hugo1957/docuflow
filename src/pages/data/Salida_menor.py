from pages.utils.inputs import create_input_field, create_dropdown_field
from pages.utils.navigation import create_footer, create_navbar_product
import flet as ft
from pages.utils.state import departamentos_data

def ViewRegistroMenores(page):
    page.controls.clear()
    page.appbar = create_navbar_product(page)[0]
    page.navigation_bar = create_footer(page)

    # Campos generales
    name_field = create_input_field("Nombres y Apellidos del Menor")
    document_field = create_input_field("Número de Identificación del Menor")
    birth_date_field = create_input_field("Fecha de Nacimiento del Menor (AAAA-MM-DD)")
    
    # Checkbox para fallecimiento
    is_father_deceased = ft.Checkbox(label="¿Padre fallecido?", on_change=lambda e: toggle_parent_fields(e, "father"))
    is_mother_deceased = ft.Checkbox(label="¿Madre fallecida?", on_change=lambda e: toggle_parent_fields(e, "mother"))
    
    father_name_field = create_input_field("Nombre del Padre", disabled=True)
    father_death_date_field = create_input_field("Fecha de Fallecimiento del Padre (AAAA-MM-DD)", disabled=True)
    
    mother_name_field = create_input_field("Nombre de la Madre", disabled=True)
    mother_death_date_field = create_input_field("Fecha de Fallecimiento de la Madre (AAAA-MM-DD)", disabled=True)
    
    # Dropdowns para departamentos y ciudades
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
                city_dropdown.options = [ft.dropdown.Option(city) for city in dept["ciudades"]]
                city_dropdown.value = None
                page.update()
                break

    # Función para habilitar/deshabilitar campos dinámicamente
    def toggle_parent_fields(e, parent_type):
        if parent_type == "father":
            father_name_field.disabled = not e.control.value
            father_death_date_field.disabled = not e.control.value
        elif parent_type == "mother":
            mother_name_field.disabled = not e.control.value
            mother_death_date_field.disabled = not e.control.value
        page.update()

    # Validación y confirmación
    def validate_and_confirm(e):
        errors = []
        if not name_field.controls[1].value.strip():
            errors.append("El campo Nombres y Apellidos del Menor es obligatorio.")
        if not document_field.controls[1].value.strip():
            errors.append("El campo Número de Identificación del Menor es obligatorio.")
        if not birth_date_field.controls[1].value.strip():
            errors.append("El campo Fecha de Nacimiento es obligatorio.")
        if is_father_deceased.value:
            if not father_name_field.controls[1].value.strip():
                errors.append("Debe ingresar el Nombre del Padre.")
            if not father_death_date_field.controls[1].value.strip():
                errors.append("Debe ingresar la Fecha de Fallecimiento del Padre.")
        if is_mother_deceased.value:
            if not mother_name_field.controls[1].value.strip():
                errors.append("Debe ingresar el Nombre de la Madre.")
            if not mother_death_date_field.controls[1].value.strip():
                errors.append("Debe ingresar la Fecha de Fallecimiento de la Madre.")
        if not department_dropdown.value:
            errors.append("Debe seleccionar un Departamento.")
        if not city_dropdown.value:
            errors.append("Debe seleccionar una Ciudad.")
        
        if errors:
            ft.dialog.AlertDialog(
                title=ft.Text("Errores de Validación"),
                content=ft.Text("\n".join(errors)),
            ).open()
        else:
            show_confirmation_dialog()

    def show_confirmation_dialog():
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Guardado"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Nombres del Menor: {name_field.controls[1].value}"),
                    ft.Text(f"Documento del Menor: {document_field.controls[1].value}"),
                    ft.Text(f"Fecha de Nacimiento: {birth_date_field.controls[1].value}"),
                    ft.Text(f"Departamento: {department_dropdown.value}"),
                    ft.Text(f"Ciudad: {city_dropdown.value}"),
                    ft.Text(f"Padre fallecido: {'Sí' if is_father_deceased.value else 'No'}"),
                    ft.Text(f"Nombre del Padre: {father_name_field.controls[1].value}" if is_father_deceased.value else ""),
                    ft.Text(f"Fecha de Fallecimiento del Padre: {father_death_date_field.controls[1].value}" if is_father_deceased.value else ""),
                    ft.Text(f"Madre fallecida: {'Sí' if is_mother_deceased.value else 'No'}"),
                    ft.Text(f"Nombre de la Madre: {mother_name_field.controls[1].value}" if is_mother_deceased.value else ""),
                    ft.Text(f"Fecha de Fallecimiento de la Madre: {mother_death_date_field.controls[1].value}" if is_mother_deceased.value else ""),
                ],
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: close_dialog(dlg)),
                ft.TextButton("Confirmar", on_click=lambda _: save_data(dlg)),
            ],
        )
        if page.overlay:
            page.overlay.pop()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def save_data(dlg):
        close_dialog(dlg)
        page.go("/data_view")

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
        content=ft.Text("Guardar", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        padding=ft.padding.all(10),
    )

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
                        name_field,
                        birth_date_field,
                        document_field,
                        ft.Row([is_father_deceased, is_mother_deceased]),
                        father_name_field,
                        father_death_date_field,
                        mother_name_field,
                        mother_death_date_field,
                        ft.Column(
                            controls=[
                                ft.Text("Departamento de Residencia"),
                                department_dropdown,
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Ciudad de Residencia"),
                                city_dropdown,
                            ],
                        ),
                        save_button,
                    ],
                ),
            )
        ],
    )
    return container
