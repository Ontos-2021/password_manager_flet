import flet as ft
from passwords import generate_password, save_password

def generator_page(master_key, page):
    """Pantalla para generar contraseñas seguras."""
    # Entradas de usuario
    seed_field = ft.TextField(label="Semilla", width=300)
    platform_field = ft.TextField(label="Plataforma", width=300)
    length_field = ft.TextField(label="Longitud", value="16", width=100)
    iterations_field = ft.TextField(label="Iteraciones", value="1", width=100)

    # Opciones de caracteres
    use_uppercase = ft.Checkbox(label="Mayúsculas", value=True)
    use_lowercase = ft.Checkbox(label="Minúsculas", value=True)
    use_digits = ft.Checkbox(label="Números", value=True)
    use_specials = ft.Checkbox(label="Especiales", value=False)

    # Resultado
    result_field = ft.TextField(label="Contraseña generada", read_only=True, width=400)

    # Botones
    def generate(e):
        try:
            password = generate_password(
                seed_field.value.strip(),
                platform_field.value.strip(),
                length=int(length_field.value),
                iterations=int(iterations_field.value),
                use_uppercase=use_uppercase.value,
                use_lowercase=use_lowercase.value,
                use_digits=use_digits.value,
                use_specials=use_specials.value,
            )
            result_field.value = password
        except Exception as ex:
            result_field.value = f"Error: {ex}"
        page.update()

    def save(e):
        if result_field.value and seed_field.value and platform_field.value:
            save_password(
                seed_field.value.strip(),
                platform_field.value.strip(),
                f"Contraseña para {platform_field.value.strip()}",
                result_field.value,
                int(iterations_field.value),
                master_key
            )
            result_field.value = "Contraseña guardada correctamente"
        else:
            result_field.value = "Por favor completa todos los campos"
        page.update()

    page.add(
        ft.Column(
            [
                seed_field,
                platform_field,
                ft.Row([length_field, iterations_field]),
                ft.Row([use_uppercase, use_lowercase, use_digits, use_specials]),
                ft.ElevatedButton("Generar", on_click=generate),
                result_field,
                ft.ElevatedButton("Guardar", on_click=save),
            ],
            spacing=10,
        )
    )
