import flet as ft
from passwords import import_passwords_from_csv


def import_page(master_key, page):
    """
    Pantalla para importar contraseñas desde un archivo CSV.
    - master_key: Clave maestra para descifrar las contraseñas.
    - page: Página de Flet.
    """
    # Campo de entrada para la ruta del archivo
    import_file_field = ft.TextField(label="Ruta para importar (CSV)", width=400)
    # Mensajes de estado
    message = ft.Text()

    # Función para manejar el botón de importar
    def import_csv(e):
        file_path = import_file_field.value.strip()  # Obtiene la ruta del archivo
        if file_path:
            try:
                import_passwords_from_csv(master_key, file_path)  # Llama a la función de importación
                message.value = f"Contraseñas importadas correctamente desde {file_path}."
            except Exception as ex:
                message.value = f"Error al importar: {ex}"
        else:
            message.value = "Por favor proporciona una ruta válida."
        page.update()

    # Componentes de la página
    page.add(
        ft.Column(
            [
                import_file_field,
                ft.ElevatedButton("Importar", on_click=import_csv),
                message,
            ],
            spacing=10,
        )
    )
