import flet as ft
import flet.canvas as cv
from PIL import Image, ImageDraw
import io


class State:
    x: float
    y: float
    drawing: list


state = State()


def ViewFirma(page):
    state.drawing = []

    def pan_start(e: ft.DragStartEvent):
        state.x = e.local_x
        state.y = e.local_y

    def pan_update(e: ft.DragUpdateEvent):
        line = cv.Line(
            state.x, state.y, e.local_x, e.local_y, paint=ft.Paint(stroke_width=3)
        )
        cp.shapes.append(line)
        state.drawing.append(((state.x, state.y), (e.local_x, e.local_y)))
        cp.update()
        state.x = e.local_x
        state.y = e.local_y

    def clear_canvas(e):
        # Limpiar las formas, pero restaurar el fondo
        cp.shapes.clear()
        cp.shapes.append(
            cv.Fill(
                ft.Paint(
                    gradient=ft.PaintLinearGradient(
                        (0, 0), (600, 600), colors=[ft.Colors.CYAN_50, ft.Colors.GREY]
                    )
                )
            )
        )
        cp.update()
        state.drawing = []

    def save_signature(e):
        if not state.drawing:
            page.snack_bar = ft.SnackBar(ft.Text("No hay firma para guardar"))
            page.snack_bar.open = True
            page.update()
            return

        # Crear una imagen en blanco
        img = Image.new("RGB", (600, 600), "white")
        draw = ImageDraw.Draw(img)

        # Dibujar las líneas en la imagen
        for line in state.drawing:
            draw.line([line[0], line[1]], fill="black", width=3)

        # Guardar la imagen en PNG
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Guardar el archivo en el sistema de archivos
        with open("firma.png", "wb") as f:
            f.write(buffer.read())

        page.snack_bar = ft.SnackBar(ft.Text("Firma guardada como 'firma.png'"))
        page.snack_bar.open = True
        page.update()

    # Crear el lienzo
    cp = cv.Canvas(
        [
            cv.Fill(
                ft.Paint(
                    gradient=ft.PaintLinearGradient(
                        (0, 0), (600, 600), colors=[ft.Colors.CYAN_50, ft.Colors.GREY]
                    )
                )
            ),
        ],
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
        expand=False,
    )

    # Botones para borrar y guardar
    buttons = ft.Row(
        [
            ft.ElevatedButton("Borrar", on_click=clear_canvas),
            ft.ElevatedButton("Guardar Firma", on_click=save_signature),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    container = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                alignment=ft.alignment.center,
                content=cp,
                border_radius=5,
                width=600,
                height=300,
            ),
            buttons,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return container
