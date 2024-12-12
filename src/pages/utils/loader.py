import flet as ft
import requests
from threading import Thread

image_cache = {}

def load_image(page, container, image_url, fit):
    def set_animated_switcher_content(new_content):
        if container.content is None or not isinstance(container.content, ft.AnimatedSwitcher):
            animated_switcher = ft.AnimatedSwitcher(
                new_content,
                transition=ft.AnimatedSwitcherTransition.SCALE,
                duration=300,
                reverse_duration=300,
                switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
                switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
            )
            container.content = animated_switcher
        else:
            container.content.content = new_content
        page.update()

    if image_url in image_cache:
        set_animated_switcher_content(image_cache[image_url])
        return
    
    def _load_image():
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = ft.Image(
                src=image_url,
                width=container.width - 20,
                height=container.height - 20,
                fit=fit,
                border_radius=ft.border_radius.all(10),
                expand=True,
            )
            image_cache[image_url] = image
            
            new_content = ft.Container(
                content=image,
                padding=ft.padding.all(10),
                opacity=0.0,
                animate_opacity=300
            )
            set_animated_switcher_content(new_content)
            new_content.opacity = 1.0
        except requests.exceptions.RequestException as e:
            print(f"Error loading image: {e}")
            error_content = ft.Text("Error loading image", color=ft.Colors.RED)
            set_animated_switcher_content(error_content)
        finally:
            page.update()

    loader = ft.ProgressRing(width=50, height=50, stroke_width=5)
    set_animated_switcher_content(
        ft.Container(
            content=loader,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )
    )
    
    Thread(target=_load_image).start()
