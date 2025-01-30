import flet as ft
from passwords import import_passwords_from_csv

def import_page(master_key, page):
    """
    Pantalla para importar contraseñas desde un archivo CSV.
    """
    message = ft.Text()

    # Crear FilePicker una sola vez
    file_picker = ft.FilePicker()

    # Asegurarse de que se agrega a la página
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)
        page.update()

    def handle_file_selection(result):
        if result.files:
            file_path = result.files[0].path
            print(f"Archivo seleccionado: {file_path}")
            try:
                import_passwords_from_csv(master_key, file_path)
                message.value = f"Contraseñas importadas correctamente desde {file_path}."
            except Exception as ex:
                message.value = f"Error al importar: {ex}"
        else:
            print("No se seleccionó ningún archivo.")
            message.value = "No se seleccionó ningún archivo."
        page.update()

    # Asignar el manejador de eventos
    file_picker.on_result = handle_file_selection

    def pick_file(e):
        print("Mostrando cuadro de diálogo para seleccionar archivo...")
        file_picker.pick_files(allow_multiple=False)  # Llamamos a la selección de archivo

    # Componentes de la página
    page.add(
        ft.Column(
            [
                ft.ElevatedButton("Seleccionar archivo CSV para importar", on_click=pick_file),
                message,
            ],
            spacing=10,
        )
    )
