import flet as ft
from passwords import export_passwords_to_csv

def export_page(master_key, page):
    """
    Pantalla para exportar contraseñas a un archivo CSV.
    """
    message = ft.Text()

    # Crear FilePicker una sola vez
    file_picker = ft.FilePicker()

    # Asegurarse de que se agrega a la página
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)
        page.update()

    def handle_folder_selection(result):
        if result.path:
            folder_path = result.path
            file_path = f"{folder_path}/contraseñas_exportadas.csv"
            print(f"Carpeta seleccionada: {folder_path}")
            try:
                export_passwords_to_csv(master_key, file_path)
                message.value = f"Contraseñas exportadas correctamente a {file_path}."
            except Exception as ex:
                message.value = f"Error al exportar: {ex}"
        else:
            print("No se seleccionó ninguna carpeta.")
            message.value = "No se seleccionó ninguna carpeta."
        page.update()

    # Asignar el manejador de eventos
    file_picker.on_result = handle_folder_selection

    def pick_folder(e):
        print("Mostrando cuadro de diálogo para seleccionar carpeta...")
        file_picker.get_directory_path()  # Llamamos a la selección de carpeta

    # Componentes de la página
    page.add(
        ft.Column(
            [
                ft.ElevatedButton("Seleccionar carpeta para exportar CSV", on_click=pick_folder),
                message,
            ],
            spacing=10,
        )
    )
