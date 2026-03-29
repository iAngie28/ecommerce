## 1. Arquitectura de Autenticación (SSO Multi-tenant)

El sistema utiliza un patrón de **Single Sign-On (SSO) basado en subdominios**. Debido a que las políticas de seguridad de los navegadores aíslan el almacenamiento local (`localStorage`) por dominio, el login requiere un flujo de transporte de token desde el portal global (`localhost`) hacia la bóveda de la tienda específica (`cliente1.localhost`).

> **💡 Nota para devs (Laravel / Web):** > En Laravel estándar, solemos usar sesiones basadas en cookies que pueden compartirse entre subdominios modificando el `SESSION_DOMAIN` en el `.env`. Sin embargo, aquí usamos una arquitectura desacoplada (React + API REST). El frontend usa `localStorage` para guardar el token JWT (similar a usar Laravel Sanctum o Passport). Como el navegador prohíbe por seguridad que `cliente1.localhost` lea el `localStorage` de `localhost`, tenemos que pasar el token explícitamente a través de la URL durante una redirección y "atraparlo" del otro lado.

## 2. Configuración en el Backend (Django)

El backend es el encargado de verificar las credenciales y determinar a qué subdominio pertenece el usuario.

**Directorio:** `\backend\`

1. **Configuración de Seguridad Base (`config/settings.py`):**
    
    - Configuración de `ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.localhost']` para permitir peticiones desde cualquier subdominio.
        
    - Definición de un modelo de usuario global: `AUTH_USER_MODEL = 'customers.Usuario'`.
        
    - Integración de `rest_framework_simplejwt` para la emisión de tokens JWT.
        
    
    > **💡 Equivalencia en Laravel:** `settings.py` es el equivalente a los archivos dentro de la carpeta `/config` y tu `.env`. `AUTH_USER_MODEL` es como decirle a Laravel en `config/auth.py` que use un modelo distinto al `App\Models\User` predeterminado.
    
2. **Personalización del Serializador de Tokens (`customers/serializers.py`):**
    
    - Creación de `MyTokenObtainPairSerializer` (heredado de SimpleJWT).
        
    - Uso: Inyectar el subdominio del tenant en la respuesta JSON del login para que React sepa hacia dónde redirigir al usuario.
        
    - Ejecución interna:
        
        ```
        # Se extrae el esquema del usuario autenticado y se inyecta en la respuesta
        token['subdomain'] = user.tenant.schema_name
        ```
        
    
    > **💡 Equivalencia en Laravel:** Un Serializador en Django REST Framework hace exactamente lo mismo que un **API Resource** o un **Eloquent Resource** (`JsonResource`) en Laravel. Toma un modelo de base de datos y lo transforma en JSON, permitiéndote añadir campos calculados al vuelo (como el `subdomain`).
    
3. **Exposición del Endpoint (`config/urls.py`):**
    
    - Mapeo de la vista personalizada al endpoint de autenticación.
        
    - Ejecución interna:
        
        ```
        path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
        ```
        
    
    > **💡 Equivalencia en Laravel:** Este archivo es exactamente tu `routes/api.php`. Mapeas una URL a un "Controller" (que en Django se llama View o ViewSet).
    

## 3. Creación y Emisión de Login en Frontend (Portal Global)

El usuario siempre inicia sesión en el dominio principal agnóstico (`localhost:3000/login`).

**Directorio:** `\frontend\src\components\`

1. **Creación del Componente Visual (`Login.js`):**
    
    - Uso de hooks de React (`useState`) para capturar las credenciales ingresadas en los inputs.
        
    - Estructuración de un formulario con un evento `onSubmit` para prevenir la recarga de la página y procesar los datos de forma asíncrona.
        
2. **Lógica de Autenticación y Salto Dinámico (SSO):**
    
    - Envío de petición `POST` con `username` y `password` al endpoint `/api/token/` configurado en el backend.
        
    - Recepción del `access_token` y el `subdomain` exacto (ej: `cliente1`).
        
    - **Redirección Dinámica:** En lugar de hacer un ruteo normal o guardar el token en el `localStorage` global, el sistema empaca el token en la barra de direcciones y envía al usuario de forma forzada al subdominio.
        
    - Ejecución interna de la función de Login:
        
        ```
        import React, { useState } from 'react';
        import api from '../services/api';
        
        function Login() {
            const [user, setUser] = useState('');
            const [pass, setPass] = useState('');
        
            const handleLogin = async (e) => {
                e.preventDefault();
                try {
                    const res = await api.post('/token/', { username: user, password: pass });
                    const { access, subdomain } = res.data;
        
                    // Salto hacia la "aduana" del cliente con el token en la URL
                    // Nota: Esto es un redireccionamiento forzado del navegador, no un enrutamiento interno de React.
                    window.location.href = `http://${subdomain}:3000/sso?token=${access}`;
                } catch (error) {
                    alert("Credenciales incorrectas o problema de conexión");
                }
            };
        
            return (
                <form onSubmit={handleLogin}>
                    <input type="text" onChange={e => setUser(e.target.value)} required />
                    <input type="password" onChange={e => setPass(e.target.value)} required />
                    <button type="submit">Entrar al Sistema</button>
                </form>
            );
        }
        export default Login;
        ```
        

## 4. Recepción y Sincronización (Subdominio del Cliente)

Una vez que el usuario aterriza en el subdominio (ej: `cliente1.localhost:3000`), el sistema debe asegurar el token antes de mostrar información sensible.

**Directorio:** `\frontend\src\`

1. **Componente de Intercepción (`App.js` -> `SSOReceiver`):**
    
    - Actúa como una "aduana". Es una ruta dedicada (`/sso`) que intercepta al usuario antes de que llegue al Dashboard.
        
    - Uso: Extraer el token de la URL de forma segura y guardarlo en la bóveda aislada (`localStorage`) del subdominio actual.
        
2. **Limpieza y Acceso (`App.js` -> `SSOReceiver`):**
    
    - Tras guardar el token, el componente borra el historial de la URL por seguridad y permite el acceso final.
        
    - Ejecución interna:
        
        ```
        const token = params.get('token');
        if (token) {
            localStorage.setItem('access_token', token);
            navigate('/dashboard', { replace: true }); // Salto limpio al Dashboard
        }
        ```
        
3. **Protección de Rutas (`App.js` -> `PrivateRoute`):**
    
    - Verifica de forma estricta que exista un `access_token` en el disco duro local antes de renderizar el componente destino (`Dashboard`).
        
    
    > **💡 Equivalencia en Web Dev:** Esto es el equivalente en frontend a aplicar un middleware de ruta `auth` en Laravel. Si no hay sesión/token, aborta la carga del controlador (Componente React) y devuelve al usuario al login.
    

## 5. Consumo de la API Protegida

Con el usuario ya establecido de forma segura dentro del subdominio, las peticiones HTTP deben apuntar al backend correcto.

**Directorio:** `\frontend\src\services\`

1. **Configuración del Cliente HTTP (`api.js`):**
    
    - Uso: Configurar Axios para que la URL base (`baseURL`) sea dinámica y lea el subdominio en el que está parado el usuario.
        
    - Ejecución interna:
        
        ```
        baseURL: `http://${window.location.hostname}:8000/api`
        ```
        
        _(Si el usuario está en `cliente1.localhost:3000`, Axios preguntará a `cliente1.localhost:8000`)._
        
2. **Interceptor de Autorización (`api.js`):**
    
    - Se intercepta cada petición saliente (ej: `api.get('/productos/')`) para adjuntar el JWT en los Headers HTTP.
        
    - Ejecución interna:
        
        ```
        const token = localStorage.getItem('access_token');
        if (token) config.headers.Authorization = `Bearer ${token}`;
        ```
        
    - Resultado: El middleware de `django-tenants` en el backend recibe la petición, identifica el host (`cliente1.localhost`), valida el JWT de la cabecera, **cambia dinámicamente el esquema de PostgreSQL a `cliente1`** (es como si Laravel hiciera un `Config::set('database.connections.tenant')` al vuelo) y devuelve los productos correctos sin mezclar datos.