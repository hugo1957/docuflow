import flet as ft
import datetime

class DatePickerField(ft.UserControl):
    def __init__(self, name="Fecha", first_date=None, last_date=None, on_change=None):
        super().__init__()
        self.name = name
        self.value = None
        self.first_date = first_date or datetime.datetime(year=1900, month=1, day=1)
        self.last_date = last_date or datetime.datetime(year=2100, month=12, day=31)
        self.on_change = on_change 
        self.text_label = ft.Text(
            self.name,
            color="#717171",
            size=14,
            weight=ft.FontWeight.NORMAL,
        )
        self.text_field = ft.TextField(
            hint_text="Seleccione una fecha",
            read_only=True,
            border_radius=ft.border_radius.all(15),
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.WHITE,
            border_color="#717171",
            border_width=0.5,
            on_click=self.open_date_picker,
        )

    def open_date_picker(self, e):
        date_picker = ft.DatePicker(
            first_date=self.first_date,
            last_date=self.last_date,
            help_text="Seleccione una fecha",
            confirm_text="Aceptar",
            cancel_text="Cancelar",
            on_change=self.update_date_field,
        )
        self.page.overlay.append(date_picker)
        date_picker.open = True
        self.page.update()

    def update_date_field(self, e):
        if e.control.value:
            self.value = e.control.value.strftime("%Y-%m-%d")
            self.text_field.value = self.value
            self.update()
            if self.on_change:
                self.on_change(self.value)

    def set_limits(self, first_date=None, last_date=None):
        if first_date:
            self.first_date = first_date
        if last_date:
            self.last_date = last_date

    def build(self):
        return ft.Column(
            controls=[
                self.text_label,
                self.text_field,
            ],
            spacing=5,
        )
