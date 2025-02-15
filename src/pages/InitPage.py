import asyncio
import flet as ft
from controls.google_signin import GoogleSignIn
from pages.endpoints.Images import image_init
import flet_lottie as fl
API_URL = "http://localhost:8000"


def GoogleLoginButton(page):
    # Instancia el control personalizado
    google_sign_in = GoogleSignIn(client_id="1035591472031-4l3v3ej2dldvach1chuog8i5i9777pp4.apps.googleusercontent.com")

    # Manejo de éxito
    def on_sign_in_success(event):
        data = event.data  # Datos del usuario desde el evento
        print(f"Inicio de sesión exitoso: {data}")
        show_modal(data)

    # Manejo de errores
    def on_sign_in_error(event):
        print(f"Error durante el inicio de sesión: {event.data}")

    # Modal para mostrar los datos
    def show_modal(data):
        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Inicio de sesión exitoso"),
            content=ft.Text(f"Bienvenido {data['displayName']} ({data['email']})"),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_modal(modal)),
            ],
        )
        page.overlay.append(modal)
        modal.open = True
        page.update()

    def close_modal(modal):
        modal.open = False
        page.update()

    # Asocia los eventos
    # google_sign_in.on_sign_in_success(on_sign_in_success)
    # google_sign_in.on_sign_in_error(on_sign_in_error)

    # page.controls.append(google_sign_in)
    
    return ft.Container(
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(15),
        height=50,
        bgcolor=ft.Colors.BLUE,
        content=ft.Row(
            controls=[
                fl.Lottie(
                    src="https://creativeferrets.com/assets/lottie/google.json",
                    width=30,
                    height=30,
                ),
                ft.Text(
                    "Continúa con Google",
                    size=15,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=lambda _: google_sign_in.sign_in(),  # Llama al método
    )





def AppleLoginButton(page):
    return ft.Container(
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(15),
        height=50,
        bgcolor=ft.Colors.BLACK,
        content=ft.Row(
            controls=[
                fl.Lottie(src="https://creativeferrets.com/assets/lottie/apple.json",
                          animate=True, width=30, height=30),
                ft.Text("Continúa con Apple", size=15,
                        color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


def WelcomeView(page: ft.Page):
    page.controls.clear()
    page.appbar = ft.CupertinoAppBar(bgcolor=ft.Colors.WHITE, visible=False)
    page.update()

    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        [
                            ft.Image(src="flags/co.png", width=20),
                            ft.Text("Colombia", color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    bgcolor=ft.Colors.BLACK12,
                    width=120,
                ),
                ft.Text(
                    "Regístrate y simplifica tu vida",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.padding.all(20),
        expand=True,
        alignment=ft.alignment.center,
    )

    def create_buttons() -> ft.Control:
        buttons = []
        buttons.append(
            ft.Container(
                alignment=ft.alignment.center,
                on_click=lambda _: page.go("/phone-register"),
                border_radius=ft.border_radius.all(15),
                height=50,
                bgcolor=ft.Colors.GREEN,
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PHONE, color=ft.Colors.WHITE),
                        ft.Text("Continúa con tu celular", size=15,
                                color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        )
        if page.platform == ft.PagePlatform.IOS:
            buttons.append(
                AppleLoginButton(page),
            )
        if page.platform == ft.PagePlatform.ANDROID:
            buttons.append(GoogleLoginButton(page))
        if page.platform not in [ft.PagePlatform.IOS, ft.PagePlatform.ANDROID]:
            buttons.extend(
                [
                    GoogleLoginButton(page),
                    AppleLoginButton(page),
                ]
            )
        buttons.append(
            ft.TextButton(
                "Soy usuario registrado",
                style=ft.ButtonStyle(color=ft.Colors.GREEN),
                on_click=lambda _: page.go("/phone-login"),
            )
        )
        return ft.AnimatedSwitcher(
            content=ft.Column(
                controls=buttons,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
        )

    main_container = ft.Container(
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        image_fit=ft.ImageFit.COVER,
        image_src="",
        content=ft.Column(
            [
                header,
                create_buttons(),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )

    async def fetch_init_image():
        data = await image_init(page)
        if data and data.get("image"):
            image_url = data["image"]
            main_container.image_src = f"{API_URL}{image_url}"
            page.update()

    async def load_user_data():
        try:
            has_token = await page.client_storage.contains_key_async("creativeferrets.tienda.access_token")
            if has_token:
                user = await page.client_storage.get_async("creativeferrets.tienda.user")
                if user:
                    page.go("/home")
        except asyncio.TimeoutError:
            print("Error loading user data: Timeout occurred")
        except Exception as e:
            print(f"Error loading user data: {e}")
    
    page.run_task(fetch_init_image)
    page.run_task(load_user_data)
    return main_container
