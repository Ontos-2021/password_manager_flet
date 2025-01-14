import flet as ft
from passwords import get_passwords, remove_password

def manager_page(master_key, page):
    """
    Pantalla para gestionar contraseñas almacenadas.
    - master_key: Clave maestra para descifrar las contraseñas.
    - page: Página principal de Flet.
    """
    # Elementos de la interfaz
    search_field = ft.TextField(label="Buscar por plataforma o descripción", width=300)
    password_list = ft.Column(scroll="adaptive")

    # Función para cargar contraseñas
    def load_passwords():
        """Carga las contraseñas almacenadas y las muestra en la lista."""
        password_list.controls.clear()
        passwords = get_passwords(master_key)
        query = search_field.value.lower().strip()

        for record in passwords:
            id_, seed, platform, description, password, iterations, created_at = record
            if query in platform.lower() or query in description.lower():
                # Añadir cada contraseña como una fila en la lista
                password_list.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"{description} ({platform})", expand=1),  # Descripción y plataforma
                            ft.Text(password),  # Contraseña descifrada o mensaje de error
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                tooltip="Copiar contraseña",
                                on_click=lambda e, pwd=password: page.set_clipboard(pwd),  # Copiar al portapapeles
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Eliminar contraseña",
                                on_click=lambda e, pwd_id=id_: delete_and_reload(pwd_id),  # Eliminar contraseña
                            ),
                        ]
                    )
                )
        page.update()

    # Función para eliminar contraseñas
    def delete_and_reload(password_id):
        """Elimina una contraseña y recarga la lista."""
        remove_password(password_id)
        load_passwords()

    # Buscar contraseñas al escribir en el campo de búsqueda
    search_field.on_change = lambda e: load_passwords()

    # Agregar los elementos a la página
    page.add(
        ft.Column(
            [
                ft.Text("Gestión de Contraseñas", weight="bold", size=20),  # Título de la página
                search_field,
                password_list,  # Lista de contraseñas
            ],
            spacing=10,
        )
    )

    # Cargar las contraseñas al abrir la página
    load_passwords()
