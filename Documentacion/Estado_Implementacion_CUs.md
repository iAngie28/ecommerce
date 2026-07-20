# Estado de Implementación - Nuevos Casos de Uso

Este documento rastrea el progreso de la programación (Backend y Frontend) de los nuevos Casos de Uso propuestos para el proyecto E-Commerce. Sirve como hoja de ruta para completar el desarrollo.

| Caso de Uso | Frontend (React) | Móvil (Flutter) | Backend (Django) | Estado Global |
|-------------|------------------|-----------------|------------------|---------------|
| **CU24 - Reseñas y Valoraciones** | ✅ Implementado | ✅ Implementado | ✅ Implementado | 🟢 Terminado |
| **CU25 - Lista de Deseos (Wishlist)**| ✅ Implementado | ✅ Implementado | ✅ Implementado | 🟢 Terminado |
| **CU26 - Programa de Fidelización** | ✅ Implementado | ✅ Implementado | ✅ Implementado | 🟢 Terminado |

---

## Detalles Técnicos

### CU24 - Reseñas y Valoraciones
* **Frontend (React - ✅ Terminado):** Se construyeron los componentes visuales `StarRating`, `ReseñaCard` y la vista `SeccionReseñas` con su respectivo CSS.
* **Móvil (Flutter - ✅ Terminado):** Se construyeron en Dart los widgets `StarRating`, `ResenaCard` y la vista embebible `SeccionResenas` junto con su conexión a la API mediante `ResenaService`.
* **Backend (Django - ✅ Terminado):** Se crearon los modelos SQL (`Reseña`), los endpoints REST (crear, moderar, listar por producto) y la lógica de negocio (`ReseñaService`) que valida que el usuario realmente haya comprado el producto (verificando en las Facturas).

### CU25 - Wishlist (Lista de Deseos)
* **Frontend (React - ✅ Terminado):** Se creó la página completa `/wishlist` (`WishlistPage.jsx`), el botón reutilizable del corazón (`WishlistButton.jsx` con animaciones CSS) y el Hook personalizado (`useWishlist.js`) para manejar las llamadas a la API.
* **Móvil (Flutter - ✅ Terminado):** Se programaron en Dart la pantalla principal `WishlistScreen`, el widget animado `WishlistButton` (corazón), y el modelo/servicio (`WishlistService`) para consumir la API.
* **Backend (Django - ✅ Terminado):** Se crearon los modelos (`Wishlist`, `WishlistItem`), la lógica de negocio (`WishlistService`), los endpoints REST y un *signal* que notifica al cliente si un producto de su lista baja de precio.

### CU26 - Programa de Fidelización (Puntos)
* **Frontend (React - ✅ Terminado):** Se creó la página "Mi Billetera de Puntos" (`MiBilleteraPuntos.jsx`) con un diseño moderno de doble panel para ver el saldo y el historial de transacciones. Además, se implementó el custom hook `useFidelizacion.js` con soporte para mock API.
* **Móvil (Flutter - ✅ Terminado):** Se programaron en Dart los modelos (`cuenta_puntos.dart`), el servicio HTTP (`fidelizacion_service.dart`) con mock API, y la interfaz visual nativa `BilleteraPuntosScreen` que muestra la tarjeta de saldo con un gradiente interactivo y el historial de transacciones.
* **Backend (Django - ✅ Terminado):** Se crearon los modelos de billetera virtual (`CuentaPuntos`, `HistorialPuntos`), la matemática de conversión (Service con bloqueos `select_for_update`), signals post_save que suman puntos al cambiar un Pedido a "ENTREGADO", y la validación de canje.
