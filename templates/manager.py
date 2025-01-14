import flet as ft
from passwords import get_passwords, remove_password

def manager_page(master_key, page):
    """Pantalla para gestionar contraseñas almacenadas."""
    search_field = ft.TextField(label="Buscar", width=300)
    password_list = ft.Column(scroll="adaptive")

    def load_passwords():
        """Carga las contraseñas almacenadas en la base de datos."""
        password_list.controls.clear()
        passwords = get_passwords(master_key)
        query = search_field.value.lower().strip()
        for id_, seed, platform, description, password, iterations, created_at in passwords:
            if query in platform.lower() or query in description.lower():
                password_list.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"{description} ({platform})", expand=1),
                            ft.Text(password),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                tooltip="Copiar contraseña",
                                on_click=lambda e, pwd=password: page.set_clipboard(pwd),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Eliminar",
                                on_click=lambda e, pwd_id=id_: delete_and_reload(pwd_id),
                            ),
                        ]
                    )
                )
        page.update()

    def delete_and_reload(password_id):
        """Elimina una contraseña y recarga la lista."""
        remove_password(password_id)
        load_passwords()

    search_field.on_change = lambda e: load_passwords()
    page.add(ft.Column([search_field, password_list]))
    load_passwords()
