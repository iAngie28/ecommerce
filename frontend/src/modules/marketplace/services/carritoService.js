import api from 'core/services/api';

const CART_KEY = 'miqhatu_carrito_efimero';

export const getLocalCart = () => {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY) || '[]');
  } catch {
    return [];
  }
};

export const saveLocalCart = (items) => {
  localStorage.setItem(CART_KEY, JSON.stringify(items));
};

export const clearLocalCart = () => {
  localStorage.removeItem(CART_KEY);
};

export const addLocalCartItem = (producto) => {
  const items = getLocalCart();
  const productoId = producto.id;
  const found = items.find((item) => item.producto_id === productoId);

  if (found) {
    found.cantidad += 1;
  } else {
    items.push({
      producto_id: productoId,
      nombre: producto.nombre,
      precio: producto.precio,
      cantidad: 1,
    });
  }

  saveLocalCart(items);
  return items;
};

export const removeLocalCartItem = (productoId) => {
  const items = getLocalCart().filter((item) => item.producto_id !== productoId);
  saveLocalCart(items);
  return items;
};

export const getLocalCartTotal = (items = getLocalCart()) => {
  return items.reduce((total, item) => {
    return total + Number(item.precio || 0) * Number(item.cantidad || 0);
  }, 0);
};

export const mapServerCartItems = (carrito) => {
  return (carrito?.items || []).map((item) => ({
    producto_id: item.producto,
    nombre: item.producto_nombre,
    precio: item.producto_precio,
    cantidad: item.cantidad,
    persisted: true,
  }));
};

export const getOpenServerCart = async () => {
  const response = await api.get('/carritos/');
  const data = response.data;
  const carts = Array.isArray(data) ? data : (data.results || []);
  return carts.find((cart) => cart.estado === 'ABIERTO') || carts[0] || null;
};

export const getServerCartItems = async () => {
  const cart = await getOpenServerCart();
  if (!cart) {
    return { carrito: null, items: [] };
  }

  const detailResponse = await api.get(`/carritos/${cart.id}/`);
  const carrito = detailResponse.data;
  return {
    carrito,
    items: mapServerCartItems(carrito),
  };
};

export const addServerCartItem = async (producto, cantidad = 1) => {
  const carritoRes = await api.post('/carritos/', {});
  const carrito = carritoRes.data;

  await api.post(`/carritos/${carrito.id}/agregar-item/`, {
    producto_id: producto.id,
    cantidad,
  });

  return getServerCartItems();
};

export const removeServerCartItem = async (productoId) => {
  const carrito = await getOpenServerCart();
  if (!carrito) {
    return { carrito: null, items: [] };
  }

  await api.post(`/carritos/${carrito.id}/eliminar-item/`, {
    producto_id: productoId,
  });

  return getServerCartItems();
};

export const clearServerCart = async () => {
  const carrito = await getOpenServerCart();
  if (!carrito) {
    return { carrito: null, items: [] };
  }

  await api.post(`/carritos/${carrito.id}/vaciar/`);
  return getServerCartItems();
};

export const syncLocalCart = async () => {
  const items = getLocalCart();
  if (!items.length) {
    const serverCart = await getServerCartItems();
    return { ...serverCart, synced: 0 };
  }

  const carritoRes = await api.post('/carritos/', {});
  let carrito = carritoRes.data;

  for (const item of items) {
    await api.post(`/carritos/${carrito.id}/agregar-item/`, {
      producto_id: item.producto_id,
      cantidad: item.cantidad,
    });
  }

  const detailResponse = await api.get(`/carritos/${carrito.id}/`);
  carrito = detailResponse.data;
  clearLocalCart();
  return { carrito, items: mapServerCartItems(carrito), synced: items.length };
};
