import flet as ft  # Librería externa
from db import init_db  # Módulo interno para inicializar la base de datos
from auth import set_master_key, validate_master_key  # Módulo interno para autenticación
from templates.generator import generator_page  # Página de generación de contraseñas
from templates.manager import manager_page  # Página de gestión de contraseñas
from templates.export import export_page  # Página para exportar contraseñas
from templates.import_passwords import import_page  # Página para importar contraseñas


def main(page: ft.Page):
    page.title = "Gestor de Contraseñas Seguras"

    init_db()  # Inicializar la base de datos

    master_key = None  # Variable para almacenar la clave maestra
    master_key_field = ft.TextField(label="Clave maestra", password=True, width=300)
    message = ft.Text()

    def validate_key(e):
        nonlocal master_key
        if validate_master_key(master_key_field.value.strip()):
            master_key = master_key_field.value.strip()  # Guarda la clave maestra válida
            page.clean()  # Limpia la pantalla inicial
            render_main_page()
        else:
            message.value = "Clave maestra incorrecta"
            page.update()

    def set_key(e):
        if master_key_field.value.strip():
            set_master_key(master_key_field.value.strip())
            message.value = "Clave maestra establecida. Reinicie la aplicación."
            page.update()

    def navigate(e):
        """Maneja la navegación entre las páginas."""
        page.clean()
        if e.control.data == "generator":
            generator_page(master_key, page)
        elif e.control.data == "manager":
            manager_page(master_key, page)
        elif e.control.data == "export":
            export_page(master_key, page)
        elif e.control.data == "import":
            import_page(master_key, page)

    def render_main_page():
        """Muestra la página principal con la barra de navegación."""
        navigation_bar = ft.Row(
            [
                ft.ElevatedButton("Generar Contraseña", data="generator", on_click=navigate),
                ft.ElevatedButton("Gestionar Contraseñas", data="manager", on_click=navigate),
                ft.ElevatedButton("Exportar", data="export", on_click=navigate),
                ft.ElevatedButton("Importar", data="import", on_click=navigate),
            ]
        )
        page.add(navigation_bar)
        generator_page(master_key, page)

    # Mostrar formulario de inicio
    page.add(
        ft.Column(
            [
                master_key_field,
                ft.Row([ft.ElevatedButton("Acceder", on_click=validate_key),
                        ft.ElevatedButton("Establecer Clave Maestra", on_click=set_key)], spacing=10),
                message,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view="web_browser")
