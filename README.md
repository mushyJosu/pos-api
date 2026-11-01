# POS API

API REST de punto de venta para negocios pequeños: permite registrar usuarios, administrar un catálogo de productos y registrar ventas con descuento automático de inventario. Desarrollada como proyecto de Aplicaciones Móviles para ser consumida desde una app Android (Kotlin + Jetpack Compose).

## Demo en línea

- **API:** https://TU-SERVICIO.onrender.com
- **Documentación interactiva (Swagger):** https://TU-SERVICIO.onrender.com/docs

> La API usa un plan gratuito: si estuvo inactiva, la primera petición puede tardar cerca de un minuto en responder.

## Características

- Registro e inicio de sesión con **JWT** y contraseñas con hash **Argon2**.
- CRUD de productos con búsqueda por nombre y paginación.
- Categorías de productos.
- Ventas con **transacción atómica**: valida stock, descuenta inventario y calcula el total en el servidor.
- Cada usuario solo accede a sus propios datos.
- Respuestas siempre en JSON.

## Stack

Python · FastAPI · Uvicorn · SQLAlchemy · PostgreSQL (Supabase) · Render

## Arquitectura

Arquitectura modular por funcionalidad, con capas dentro de cada módulo:

```
app/
├── main.py
├── core/              # configuración, base de datos, seguridad
└── modules/
    ├── auth/
    ├── categories/
    ├── products/
    └── sales/
        ├── router.py      # controller: recibe y responde HTTP
        ├── service.py     # reglas de negocio
        ├── repository.py  # acceso a la base de datos
        ├── models.py      # tablas (SQLAlchemy)
        └── schemas.py     # contratos JSON (Pydantic)
```

## Endpoints

| Método | Ruta | Descripción | Requiere token |
|---|---|---|---|
| POST | `/auth/register` | Crear cuenta | No |
| POST | `/auth/login` | Obtener token | No |
| GET | `/auth/me` | Usuario actual | Sí |
| GET / POST | `/categories` | Listar / crear categorías | Sí |
| GET / POST | `/products` | Listar (con `q`, `limit`, `offset`) / crear | Sí |
| GET / PUT / DELETE | `/products/{id}` | Consultar / actualizar / eliminar | Sí |
| POST | `/sales` | Registrar una venta | Sí |
| GET | `/sales` | Listar ventas | Sí |
| GET | `/sales/{id}` | Detalle de una venta | Sí |

Ejemplo de venta:

```json
POST /sales
{ "items": [ { "product_id": 1, "quantity": 2 }, { "product_id": 3, "quantity": 1 } ] }
```

Las rutas protegidas esperan el encabezado `Authorization: Bearer <token>`.

## Ejecutar localmente

```bash
git clone https://github.com/TU_USUARIO/pos-api.git
cd pos-api
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # y completa los valores
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000/docs

## Variables de entorno

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL (`postgresql+psycopg://...`) |
| `JWT_SECRET` | Secreto largo y aleatorio para firmar tokens |
| `JWT_EXPIRE_MINUTES` | Duración del token en minutos (por defecto 60) |

## Seguridad

- Secretos solo en variables de entorno, nunca en el repositorio.
- Contraseñas almacenadas con hash Argon2.
- Tokens con expiración y algoritmo fijo.
- Validación de toda la entrada con Pydantic.
- Filtro por dueño en cada consulta (un usuario no puede ver datos de otro).
- Restricciones en la base de datos (precio y stock no negativos).
- Row Level Security activado en las tablas de Supabase.

## Mejoras futuras

- Refresh tokens y límite de intentos de login.
- Migraciones con Alembic.
- Pruebas automatizadas.
- Roles (administrador / cajero) y reportes de ventas.
- Contenedor Docker.
