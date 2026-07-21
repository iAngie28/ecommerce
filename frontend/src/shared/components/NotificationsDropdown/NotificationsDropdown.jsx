import React, { useState, useEffect, useRef } from 'react';
import { Bell, Check } from 'lucide-react';
import api from 'core/services/api';
import styles from './NotificationsDropdown.module.css';

const NotificationsDropdown = () => {
    const [open, setOpen] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [loading, setLoading] = useState(false);
    const dropdownRef = useRef(null);
    const intervalRef = useRef(null);

    const fetchNotifications = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            if (intervalRef.current) clearInterval(intervalRef.current);
            return;
        }

        try {
            setLoading(true);
            const res = await api.get('/notificaciones/', { skipAuthRedirect: true });
            const data = Array.isArray(res.data) ? res.data : res.data?.results || [];
            setNotifications(data);
            setUnreadCount(data.filter(n => !n.leido).length);
        } catch (error) {
            // Si es 401 o error de red, el token es inválido o el backend no responde, detenemos el polling
            if (error.response?.status === 401 || error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
                if (intervalRef.current) {
                    clearInterval(intervalRef.current);
                    intervalRef.current = null;
                }
            } else {
                // Solo logueamos otros errores si no son de red puros para no inundar la consola
                console.error('Error fetching notifications', error);
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNotifications();
        intervalRef.current = setInterval(fetchNotifications, 30000);
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const markAsRead = async (notif) => {
        try {
            const payload = notif.tienda_schema
                ? { leido: true, tenant_schema: notif.tienda_schema }
                : { leido: true };
            await api.patch(`/notificaciones/${notif.id}/`, payload);
            setNotifications(prev => prev.map(n => (
                n.id === notif.id && n.tienda_schema === notif.tienda_schema
                    ? { ...n, leido: true }
                    : n
            )));
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch (e) {
            console.error(e);
        }
    };

    const markAllAsRead = async () => {
        try {
            await api.post('/notificaciones/marcar-todas-leidas/');
            setNotifications(prev => prev.map(n => ({ ...n, leido: true })));
            setUnreadCount(0);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className={styles.dropdownContainer} ref={dropdownRef}>
            <div className={styles.iconBtn} onClick={() => setOpen(!open)}>
                <Bell size={20} />
                {unreadCount > 0 && (
                    <span className={styles.badge}>{unreadCount}</span>
                )}
            </div>

            {open && (
                <div className={styles.dropdownMenu}>
                    <div className={styles.header}>
                        <h3>Notificaciones</h3>
                        {unreadCount > 0 && (
                            <button onClick={markAllAsRead} className={styles.markAllBtn}>
                                <Check size={14} /> Marcar todo como leído
                            </button>
                        )}
                    </div>
                    
                    <div className={styles.list}>
                        {loading && notifications.length === 0 ? (
                            <div className={styles.empty}>Cargando...</div>
                        ) : notifications.length === 0 ? (
                            <div className={styles.empty}>No tienes notificaciones</div>
                        ) : (
                            notifications.map(notif => (
                                <div 
                                    key={`${notif.tienda_schema || 'tenant'}-${notif.id}`}
                                    className={`${styles.item} ${!notif.leido ? styles.unread : ''}`}
                                    onClick={() => !notif.leido && markAsRead(notif)}
                                >
                                    <div className={styles.itemHeader}>
                                        <span className={styles.title}>{notif.titulo}</span>
                                        <span className={styles.time}>
                                            {new Date(notif.fecha_creacion).toLocaleDateString()}
                                        </span>
                                    </div>
                                    {notif.tienda_nombre && (
                                        <span className={styles.storeName}>{notif.tienda_nombre}</span>
                                    )}
                                    <p className={styles.message}>{notif.mensaje}</p>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default NotificationsDropdown;
