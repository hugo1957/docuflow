from pages.utils.inputs import create_input_field, create_dropdown_field
from pages.utils.alert import show_construction_dialog
from pages.utils.navigation import create_footer
import flet as ft
import re
from pages.utils.json import json_base64

def validate_password_strength(password):
    if len(password) < 6:
        return "Débil"
    elif re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[!@#$%^&*]', password):
        return "Fuerte"
    else:
        return "Moderada"


def ViewRegister(page):
    page.controls.clear()
    page.navigation_bar = create_footer(page)
    password_strength_text = ft.Text("")
    password_match_text = ft.Text("")

    name_field = create_input_field("Nombres")
    last_name_field = create_input_field("Apellidos")
    type_document_field = create_dropdown_field("Tipo de Documento",options=["Cédula de Ciudadanía", "Cédula de Extranjería","Pasaporte", "Tarjeta de Identidad"])
    document_field = create_input_field("Número de Identificación")
    gender_field = create_dropdown_field("Género",options=["Masculino", "Femenino", "Otro"])
    email_field = create_input_field("E-mail")
    phone_field = create_input_field("Celular")
    password_field = ft.Column(
      controls=[
        ft.Text("Contraseña", style=ft.TextStyle(color="#717171")),
        ft.TextField(
        width=350,
        height=60,
        password=True,
        can_reveal_password=True,
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        on_change=lambda e: on_password_change(e),
    )
      ]
    )

    repeat_password_field = ft.Column(
      controls=[
        ft.Text("Repetir Contraseña", style=ft.TextStyle(color="#717171")),
        ft.TextField(
        width=350,
        height=60,
        password=True,
        can_reveal_password=True,
        border_radius=ft.border_radius.all(15),
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border_color="#717171",
        label_style=ft.TextStyle(color="#717171"),
        border_width=0.5,
        on_change=lambda e: check_password_match(e),
    )
      ]
    )

    def on_password_change(e):
        password = password_field.value
        if password == "":
            password_strength_text.value = ""
        else:
            strength = validate_password_strength(password)
            password_strength_text.value = f"Fortaleza: {strength}"
            password_strength_text.color = (
                ft.Colors.RED if strength == "Débil" else
                ft.Colors.ORANGE if strength == "Moderada" else
                ft.Colors.GREEN
            )
        page.update()

    def check_password_match(e):
        password = password_field.value
        repeat_password = repeat_password_field.value
        if password == "" or repeat_password == "":
            password_match_text.value = ""  # No mostrar nada si los campos están vacíos
        elif password == repeat_password:
            password_match_text.value = "Las contraseñas coinciden."
            password_match_text.color = ft.Colors.GREEN
        else:
            password_match_text.value = "Las contraseñas no coinciden."
            password_match_text.color = ft.Colors.RED
        page.update()

    # Contenedor principal
    container = ft.Column(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.padding.all(20),
                expand=True,
                content=ft.Column(
                    
                    scroll=ft.ScrollMode.HIDDEN,
                    controls=[
                        ft.Container(height=5),

                        ft.Text(
                            "Registro", text_align="left", size=20, weight="bold"),
                        ft.Container(height=10),

                        name_field,
                        last_name_field,
                        type_document_field,
                        document_field,
                        email_field,
                        phone_field,
                        gender_field,
                        password_field,
                        password_strength_text,
                        repeat_password_field,
                        password_match_text,
                        ft.Container(
                            alignment=ft.alignment.center,
                            # on_click=handle_login_click,
                            ink=True,
                            border_radius=ft.border_radius.all(5),
                            width=350,
                            height=50,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.Alignment(0.8, 1),
                                colors=[
                                    "#717171",
                                    "#e5bc16",
                                ],
                            ),
                            content=ft.Text(
                                "Registrate", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ),

                    
                    ]
                )
            )
        ]
    )

    return container
