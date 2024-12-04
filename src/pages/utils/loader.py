import flet as ft
import requests
from threading import Thread

# Global dictionary to cache images
image_cache = {}

def load_image(page, container, image_url, fit):
    def set_animated_switcher_content(new_content):
        if container.content is None or not isinstance(container.content, ft.AnimatedSwitcher):
            # Create the AnimatedSwitcher if it doesn't exist
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
            # Update the content of the existing AnimatedSwitcher
            container.content.content = new_content
        page.update()

    # Check if the image is already in the cache
    if image_url in image_cache:
        # Use the cached image
        set_animated_switcher_content(image_cache[image_url])
        return
    
    def _load_image():
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = ft.Image(
                src=image_url,
                width=container.width - 20,  # Account for padding
                height=container.height - 20, # Account for padding
                fit=fit,
                border_radius=ft.border_radius.all(10),
                expand=True,
            )
            # Cache the image
            image_cache[image_url] = image
            
            # Set the image content and start the fade-in animation
            new_content = ft.Container(
                content=image,
                padding=ft.padding.all(10),  # Add padding to the image
                opacity=0.0,  # Start with the image fully transparent
                animate_opacity=300  # Animation duration in milliseconds
            )
            set_animated_switcher_content(new_content)

            # Update opacity to fade in
            new_content.opacity = 1.0
        except requests.exceptions.RequestException as e:
            print(f"Error loading image: {e}")
            error_content = ft.Text("Error loading image", color=ft.Colors.RED)
            set_animated_switcher_content(error_content)
        finally:
            page.update()

    # Center the loader within the container
    loader = ft.ProgressRing(width=50, height=50, stroke_width=5)
    set_animated_switcher_content(
        ft.Container(
            content=loader,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )
    )
    
    Thread(target=_load_image).start()
