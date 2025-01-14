### **Resumen del Proyecto: Gestor de Contraseñas Seguras con Flet**

---

### **1. Descripción General**
El **Gestor de Contraseñas Seguras** es una aplicación desarrollada en **Python** utilizando **Flet** para la interfaz gráfica y **SQLite** como base de datos local. Su objetivo es permitir a los usuarios generar, gestionar y almacenar contraseñas seguras de manera local, con opciones de exportación e importación, todo protegido por una clave maestra.

---

### **2. Funcionalidades Principales**

#### **A. Generador de Contraseñas**
- Generación de contraseñas seguras basadas en una **semilla** y una **plataforma**.
- Configuración de la longitud de la contraseña y los tipos de caracteres permitidos:
  - Mayúsculas, minúsculas, dígitos, caracteres especiales.
- Opcional: Selección del número de iteraciones del algoritmo de hash (predeterminado: 1).
- Vista previa de la contraseña generada.
- Opción para guardar la contraseña en la base de datos local.

#### **B. Gestión de Contraseñas**
- Listar todas las contraseñas almacenadas:
  - Muestra: Descripción, plataforma, contraseña (descifrada temporalmente), número de iteraciones, y fecha de creación.
- Buscar contraseñas por descripción o plataforma.
- Editar la semilla, plataforma o iteraciones de una contraseña existente.
- Eliminar contraseñas seleccionadas.

#### **C. Protección con Clave Maestra**
- Una **clave maestra** protege el acceso a la aplicación.
- La clave maestra:
  - Se solicita al iniciar la aplicación.
  - Es usada para cifrar y descifrar las contraseñas almacenadas.
- En la primera ejecución, se solicita al usuario crear la clave maestra.
- La clave maestra no se almacena directamente, solo su hash.

#### **D. Exportación e Importación**
- Exportar contraseñas a un archivo **CSV**:
  - Opcional: Exportar contraseñas cifradas o descifradas.
- Importar contraseñas desde un archivo **CSV**:
  - Se verifica que los datos sean válidos.
  - Se cifra cada contraseña al importarla.

---

### **3. Estructura del Proyecto**

#### **Componentes Clave**
```plaintext
secure_password_manager/
├── main.py             # Entrada principal de la aplicación.
├── db.py               # Funciones para la gestión de la base de datos SQLite.
├── crypto.py           # Funciones de cifrado y derivación de claves.
├── auth.py             # Gestión de la clave maestra y autenticación.
├── passwords.py        # Lógica de generación y manejo de contraseñas.
├── templates/          # Componentes de la interfaz gráfica (Flet).
│   ├── generator.py    # Pantalla de generación de contraseñas.
│   ├── manager.py      # Pantalla de gestión de contraseñas.
│   ├── export.py       # Pantalla para exportar contraseñas.
│   ├── import.py       # Pantalla para importar contraseñas.
├── requirements.txt    # Dependencias del proyecto (flet, cryptography).
└── README.md           # Documentación del proyecto.
```

---

### **4. Base de Datos**

#### **Tablas Principales**

##### **Tabla `passwords`**
| Columna      | Tipo      | Descripción                                        |
|--------------|-----------|----------------------------------------------------|
| `id`         | INTEGER   | Identificador único.                               |
| `seed`       | TEXT      | Semilla de generación.                             |
| `platform`   | TEXT      | Plataforma asociada (ej., Gmail, Facebook).        |
| `description`| TEXT      | Descripción opcional (ej., "Cuenta personal Gmail").|
| `password`   | TEXT      | Contraseña generada (cifrada).                     |
| `iterations` | INTEGER   | Número de iteraciones del algoritmo de hash.       |
| `created_at` | TIMESTAMP | Fecha de creación.                                 |

##### **Tabla `settings`**
| Columna      | Tipo      | Descripción                                      |
|--------------|-----------|--------------------------------------------------|
| `id`         | INTEGER   | Identificador único.                             |
| `key_name`   | TEXT      | Nombre de la configuración (ej., "master_key").  |
| `key_value`  | TEXT      | Valor asociado (ej., hash de la clave maestra).  |

---

### **5. Flujo de la Aplicación**

#### **Primera Ejecución**
1. El sistema detecta que no existe una clave maestra.
2. Solicita al usuario crear una clave maestra.
3. Guarda un hash de la clave maestra en la base de datos.

#### **Inicios Posteriores**
1. Solicita la clave maestra al usuario.
2. Valida la clave ingresada contra el hash almacenado.
3. Si es correcta, la aplicación se desbloquea.

#### **Generación de Contraseñas**
1. El usuario ingresa la semilla y plataforma, selecciona la longitud, caracteres y número de iteraciones.
2. Genera la contraseña y decide si desea guardarla.

#### **Gestión de Contraseñas**
1. Las contraseñas guardadas se cifran con la clave derivada de la llave maestra.
2. Para listar o buscar contraseñas, se descifran temporalmente.
3. El usuario puede copiar, editar o eliminar las contraseñas.

#### **Exportación e Importación**
1. Las contraseñas pueden exportarse a un archivo CSV, cifradas o descifradas.
2. Los datos importados se verifican y se cifran al almacenarse.

---

### **6. Seguridad**

#### **Cifrado**
- Cifrado simétrico usando AES-GCM con una clave derivada de la llave maestra.
- Derivación de claves usando PBKDF2 con sal y múltiples iteraciones.

#### **Protección**
- La clave maestra no se almacena directamente, solo su hash.
- Cada contraseña almacenada se cifra con la clave derivada.

#### **Persistencia**
- Los datos se almacenan localmente en una base de datos SQLite, portátil y ligera.

---

### **7. Escalabilidad y Futuras Extensiones**

1. **Autenticación Multiusuario:**
   - Permitir múltiples usuarios con claves maestras separadas.

2. **Sincronización:**
   - Sincronizar contraseñas con un backend remoto.

3. **Aplicación Móvil:**
   - Convertir la aplicación en una Progressive Web App (PWA) para su uso en Android/iOS.

---

