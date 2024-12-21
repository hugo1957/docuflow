import flet as ft
class PhoneInputDropdown(ft.Row):
    def __init__(self, on_country_change=None, on_phone_change=None):
        super().__init__()
        self.spacing = 5
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

        self.on_country_change = on_country_change
        self.on_phone_change = on_phone_change

        # Datos de países (ejemplo reducido)
        self.country_data = {
            "+57":  {"flag": "flags/co.png", "length": 10},
            "+1":   {"flag": "flags/us.png", "length": 10},
            "+44":  {"flag": "flags/gb.png", "length": 10},
            "+93":  {"flag": "flags/af.png", "length": 9},
            "+355": {"flag": "flags/al.png", "length": 9},
            # ... continúa con tu diccionario completo ...
        }
        self.selected_country = "+57"

        # Crear controles internos
        self.dropdown = self._create_dropdown()
        self.phone_field = self._create_phone_field()

        self.controls = [self.dropdown, self.phone_field]

    def _create_dropdown(self):
        """Crea el dropdown para seleccionar el país."""
        options = [
            ft.dropdown.Option(
                key=key,
                content=ft.Row(
                    controls=[
                        ft.Image(src=value["flag"], width=20, height=20),
                        ft.Text(f"({key})", size=12, color=ft.Colors.BLACK),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            )
            for key, value in self.country_data.items()
        ]

        return ft.Dropdown(
            options=options,
            value=self.selected_country,
            width=110,
            height=60,
            border_radius=ft.border_radius.all(15),
            padding=ft.padding.all(5),
            bgcolor=ft.Colors.WHITE,
            border_width=0.5,
            on_change=self.handle_country_change,
            filled=False,
        )

    def _create_phone_field(self):
        """Crea el campo de texto para el número de teléfono."""
        max_length = self.country_data[self.selected_country]["length"]
        return ft.TextField(
            max_length=max_length,
            width=250,
            height=60,
            border_radius=ft.border_radius.all(15),
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.WHITE,
            border_color="#717171",
            label_style=ft.TextStyle(color="#717171", font_family="Poppins"),
            border_width=0.5,
            expand=True,
            filled=False,
            on_change=self.handle_phone_change,
        )

    def handle_country_change(self, e):
        """Callback para manejar el cambio de país."""
        self.selected_country = self.dropdown.value
        max_length = self.country_data[self.selected_country]["length"]
        self.phone_field.max_length = max_length

        if self.on_country_change:
            self.on_country_change(self.selected_country)

        self.update()

    def handle_phone_change(self, e):
        """Callback para manejar el cambio en el número de teléfono."""
        if self.on_phone_change:
            self.on_phone_change(self.phone_field.value)