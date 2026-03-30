# 🔍 DIAGNÓSTICO: LOGIN FALLA DESPUÉS DE LOGOUT

## Pasos para Diagnosticar:

### 1. Abre la Consola (F12)
```
Presiona: F12 en el navegador
Pestaña: Console
```

### 2. Primer Login (FUNCIONA)
- Usuario: `adm1`
- Contraseña: `123`
- ✓ Debería funcionar

### 3. Ve a Network (F12 → Network)
- Limpia el historial (click derecho → Clear all)
- Haz logout
- Intenta login nuevamente

### 4. Busca la petición POST `/token/`
- Click en esa petición
- Pestaña "Response"
- Copia TODO lo que dice

### 5. También revisa:
- **Request Headers**: ¿Qué headers se envían?
- **Request Body**: ¿Se envían username y password?
- **Response Status**: ¿200? ¿401? ¿400?
- **Console Tab**: ¿Hay errores en rojo?

---

## Qué Copiar Exactamente:

```
RESPONSE DE LA SEGUNDA PETICIÓN /token/:
[Pega aquí lo que veas]

STATUS HTTP:
[200 / 401 / 400 / 500 / otro?]

CONSOLE ERROR (si lo hay):
[Pega el error completo]

HEADERS ENVIADOS:
[Authorization: Bearer ... ? O NO tiene Auth?]
```

---

## Escenario Esperado vs Real:

**LO QUE DEBERÍA PASAR:**
```
1er Login: POST /token/ → 200 OK → {access: "...", subdomain: "cliente1"}
Logout: localStorage.clear()
2do Login: POST /token/ → 200 OK → {access: "...", subdomain: "cliente1"}
```

**LO QUE PROBABLEMENTE PASA:**
```
1er Login: ✓ 200 OK
Logout: ✓ Limpia
2do Login: ✗ 401 / 400 / 500 → "credenciales incorrectas"
```

---

## Hipótesis Posibles (por orden de probabilidad):

1. **Django rechaza username/password en 2do intento** (400 Bad Request)
   → Problema en backend, no en frontend

2. **Token anterior sigue siendo inyectado** (401 Unauthorized)
   → Problema con limpieza de localStorage

3. **CORS bloqueando en 2do intento** (error de red)
   → Problema de configuración Django

4. **UserAgent o headers cambian** (403 Forbidden)
   → Raro, pero posible

---

## Ejecuta esto en la Console (F12):

```javascript
// Comprueba si localStorage está limpio después de logout
console.log("access_token:", localStorage.getItem('access_token'));
console.log("refresh_token:", localStorage.getItem('refresh_token'));

// Debería mostrar: null / null si logout funcionó
```

---

**¿Qué ves exactamente en Network tab cuando falla el 2do login?**
