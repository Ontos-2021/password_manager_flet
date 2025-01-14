import flet as ft
from db import init_db  # Inicializar la base de datos
from auth import set_master_key, validate_master_key  # Gestión de clave maestra


def navigation_bar(master_key, page):
    """Genera la barra de navegación."""
    return ft.Row(
        [
            ft.ElevatedButton("Generar Contraseña", on_click=lambda e: navigate_to("generator", master_key, page)),
            ft.ElevatedButton("Gestionar Contraseñas", on_click=lambda e: navigate_to("manager", master_key, page)),
            ft.ElevatedButton("Exportar", on_click=lambda e: navigate_to("export", master_key, page)),
            ft.ElevatedButton("Importar", on_click=lambda e: navigate_to("import", master_key, page)),
        ]
    )


def navigate_to(page_name, master_key, page):
    """Navega a la página especificada."""
    page.clean()  # Limpia la página actual
    page.add(navigation_bar(master_key, page))  # Añade la barra de navegación
    if page_name == "generator":
        from templates.generator import generator_page
        generator_page(master_key, page)
    elif page_name == "manager":
        from templates.manager import manager_page
        manager_page(master_key, page)
    elif page_name == "export":
        from templates.export import export_page
        export_page(master_key, page)
    elif page_name == "import":
        from templates.import_passwords import import_page
        import_page(master_key, page)


def render_main_page(master_key, page):
    """Muestra la página principal con la barra de navegación."""
    page.clean()
    page.add(navigation_bar(master_key, page))  # Añade la barra de navegación
    navigate_to("generator", master_key, page)  # Página inicial: Generar Contraseña


def main(page: ft.Page):
    page.title = "Gestor de Contraseñas Seguras"

    init_db()  # Inicializar la base de datos

    master_key = None  # Clave maestra
    master_key_field = ft.TextField(label="Clave maestra", password=True, width=300)
    message = ft.Text()

    def validate_key(e):
        nonlocal master_key
        if validate_master_key(master_key_field.value.strip()):
            master_key = master_key_field.value.strip()  # Guarda la clave maestra válida
            page.clean()  # Limpia la pantalla inicial
            render_main_page(master_key, page)
        else:
            message.value = "Clave maestra incorrecta"
            page.update()

    def set_key(e):
        if master_key_field.value.strip():
            set_master_key(master_key_field.value.strip())
            message.value = "Clave maestra establecida. Reinicie la aplicación."
            page.update()

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
