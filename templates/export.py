import flet as ft
from passwords import export_passwords_to_csv  # Importar la lógica de exportación desde passwords.py

def export_page(master_key, page):
    """
    Pantalla para exportar contraseñas a un archivo CSV.
    - master_key: Clave maestra para descifrar las contraseñas.
    - page: Página principal de Flet.
    """
    # Campo de entrada para la ruta del archivo
    export_file_field = ft.TextField(label="Ruta para exportar (CSV)", width=400)
    # Mensaje de estado
    message = ft.Text()

    # Función para manejar el botón de exportar
    def export_csv(e):
        file_path = export_file_field.value.strip()  # Obtiene la ruta del archivo
        if file_path:
            try:
                export_passwords_to_csv(master_key, file_path)  # Llama a la función de exportación
                message.value = f"Contraseñas exportadas correctamente a {file_path}."
            except Exception as ex:
                message.value = f"Error al exportar: {ex}"
        else:
            message.value = "Por favor proporciona una ruta válida."
        page.update()

    # Componentes de la página
    page.add(
        ft.Column(
            [
                export_file_field,
                ft.ElevatedButton("Exportar", on_click=export_csv),
                message,
            ],
            spacing=10,
        )
    )
