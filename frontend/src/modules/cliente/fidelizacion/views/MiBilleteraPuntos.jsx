import React, { useEffect, useMemo, useState } from 'react';
import {
    AlertTriangle,
    ArrowDownCircle,
    ArrowUpCircle,
    Calculator,
    Coins,
    Gift,
    History,
    RefreshCw,
    RotateCcw,
    ShieldCheck,
} from 'lucide-react';
import { Alert, Button, Spinner } from 'shared/components';
import { AppView } from 'shared/widgets';
import useFidelizacion from '../hooks/useFidelizacion';
import styles from './MiBilleteraPuntos.module.css';

const MOVEMENT_META = {
    ACUMULACION: {
        label: 'Acumulación',
        title: 'Puntos ganados',
        Icon: ArrowUpCircle,
        className: 'gain',
    },
    CANJE: {
        label: 'Canje',
        title: 'Puntos canjeados',
        Icon: ArrowDownCircle,
        className: 'redeem',
    },
    EXPIRACION: {
        label: 'Expiración',
        title: 'Puntos expirados',
        Icon: AlertTriangle,
        className: 'expire',
    },
    REVERSO: {
        label: 'Reverso',
        title: 'Ajuste por reverso',
        Icon: RotateCcw,
        className: 'reverse',
    },
};

const formatBs = (value) => `Bs. ${Number(value || 0).toFixed(2)}`;

const formatDate = (dateString) => {
    if (!dateString) return 'Sin fecha';
    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) return 'Sin fecha';

    return date.toLocaleString('es-BO', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
};

const MiBilleteraPuntos = () => {
    const [simulatedPoints, setSimulatedPoints] = useState('');
    const { 
        cuenta, 
        loading, 
        error, 
        fetchCuenta, 
        fetchConfiguracion,
        calcularDescuento,
        calcularPuntosGanados,
    } = useFidelizacion();

    const loadData = async () => {
        await Promise.allSettled([
            fetchCuenta(),
            fetchConfiguracion(),
        ]);
    };

    useEffect(() => {
        loadData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [fetchCuenta, fetchConfiguracion]);

    const saldoActual = cuenta?.saldo_actual || 0;
    const puntosHistoricos = cuenta?.puntos_historicos || 0;
    const descuentoDisponible = calcularDescuento(saldoActual);
    const puntosPorDiezBs = calcularPuntosGanados(10);
    const simulatedDiscount = calcularDescuento(simulatedPoints);

    const sortedMovimientos = useMemo(() => {
        const movimientos = cuenta?.historial || [];
        return [...movimientos].sort((a, b) => new Date(b.fecha || 0) - new Date(a.fecha || 0));
    }, [cuenta?.historial]);

    const handleSimulatorChange = (value) => {
        const parsed = Math.floor(Number(value));
        if (!Number.isFinite(parsed) || parsed <= 0) {
            setSimulatedPoints('');
            return;
        }
        setSimulatedPoints(String(Math.min(parsed, saldoActual)));
    };

    if (loading && !cuenta) {
        return (
            <AppView title="Mis Puntos" subtitle="Saldo y movimientos de tu programa de fidelización">
                <div className={styles.stateBox}>
                    <Spinner size="lg" />
                    <p>Cargando tu billetera de puntos...</p>
                </div>
            </AppView>
        );
    }

    if (error && !cuenta) {
        return (
            <AppView title="Mis Puntos" subtitle="Saldo y movimientos de tu programa de fidelización">
                <div className={styles.stateBox}>
                    <AlertTriangle size={34} className={styles.stateIconDanger} />
                    <p>{error}</p>
                    <Button variant="secondary" leftIcon={<RefreshCw size={16} />} onClick={loadData}>
                        Reintentar
                    </Button>
                </div>
            </AppView>
        );
    }

    return (
        <AppView
            title="Mis Puntos"
            subtitle="Consulta tu saldo, equivalencia y movimientos del programa de fidelización"
            actions={(
                <Button
                    variant="secondary"
                    leftIcon={<RefreshCw size={16} />}
                    loading={loading}
                    onClick={loadData}
                >
                    Actualizar
                </Button>
            )}
        >
            {error && (
                <Alert variant="warning" title="No se pudo refrescar toda la información">
                    {error}
                </Alert>
            )}

            <section className={styles.heroPanel}>
                <div className={styles.heroContent}>
                    <span className={styles.heroIcon}>
                        <Gift size={26} />
                    </span>
                    <div>
                        <p className={styles.eyebrow}>Programa de fidelización</p>
                        <h2>{cuenta?.cliente_nombre || 'Cliente'}</h2>
                        <p className={styles.heroText}>
                            Tus puntos se acreditan cuando una compra llega a estado entregado.
                        </p>
                    </div>
                </div>
                <div className={styles.balanceBlock}>
                    <span>Saldo disponible</span>
                    <strong>{saldoActual.toLocaleString('es-BO')}</strong>
                    <small>puntos</small>
                </div>
            </section>

            <section className={styles.summaryGrid}>
                <article className={styles.summaryCard}>
                    <Coins size={20} className={styles.cardIconPrimary} />
                    <span>Equivalencia actual</span>
                    <strong>{formatBs(descuentoDisponible)}</strong>
                    <small>descuento máximo disponible</small>
                </article>

                <article className={styles.summaryCard}>
                    <History size={20} className={styles.cardIconInfo} />
                    <span>Puntos históricos</span>
                    <strong>{puntosHistoricos.toLocaleString('es-BO')}</strong>
                    <small>acumulados en tu cuenta</small>
                </article>

                <article className={styles.summaryCard}>
                    <ShieldCheck size={20} className={styles.cardIconSuccess} />
                    <span>Regla de acumulación</span>
                    <strong>{puntosPorDiezBs}</strong>
                    <small>puntos por cada Bs. 10</small>
                </article>
            </section>

            <section className={styles.contentGrid}>
                <article className={styles.panel}>
                    <div className={styles.panelHeader}>
                        <div>
                            <p className={styles.eyebrow}>Canje</p>
                            <h3>Simulador de descuento</h3>
                        </div>
                        <Calculator size={20} />
                    </div>

                    <div className={styles.simulatorBody}>
                        <label htmlFor="simulated-points">Puntos a usar</label>
                        <div className={styles.pointsInputWrap}>
                            <input
                                id="simulated-points"
                                type="number"
                                min="0"
                                max={saldoActual}
                                value={simulatedPoints}
                                placeholder="0"
                                onChange={(event) => handleSimulatorChange(event.target.value)}
                            />
                            <span>pts</span>
                        </div>
                        <input
                            className={styles.pointsRange}
                            type="range"
                            min="0"
                            max={saldoActual}
                            value={simulatedPoints || 0}
                            disabled={saldoActual === 0}
                            onChange={(event) => handleSimulatorChange(event.target.value)}
                            aria-label="Seleccionar puntos a simular"
                        />

                        <div className={styles.simulatorResult}>
                            <span>Descuento estimado</span>
                            <strong>{formatBs(simulatedDiscount)}</strong>
                        </div>
                    </div>
                </article>

                <article className={styles.panel}>
                    <div className={styles.panelHeader}>
                        <div>
                            <p className={styles.eyebrow}>Reglas</p>
                            <h3>Cómo se controlan tus puntos</h3>
                        </div>
                        <ShieldCheck size={20} />
                    </div>
                    <div className={styles.rulesList}>
                        <div>
                            <strong>Acumulación automática</strong>
                            <span>Los puntos se suman cuando el pedido se marca como entregado.</span>
                        </div>
                        <div>
                            <strong>Saldo protegido</strong>
                            <span>El sistema no permite que tu cuenta quede con saldo negativo.</span>
                        </div>
                        <div>
                            <strong>Historial inmutable</strong>
                            <span>Los movimientos son de solo lectura para preservar la auditoría.</span>
                        </div>
                    </div>
                </article>
            </section>

            <section className={styles.historyPanel}>
                <div className={styles.panelHeader}>
                    <div>
                        <p className={styles.eyebrow}>Movimientos</p>
                        <h3>Historial de puntos</h3>
                    </div>
                    <span className={styles.updatedAt}>
                        Actualizado {formatDate(cuenta?.fecha_actualizacion)}
                    </span>
                </div>

                {sortedMovimientos.length > 0 ? (
                    <div className={styles.tableWrap}>
                        <table className={styles.historyTable}>
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Referencia</th>
                                    <th>Fecha</th>
                                    <th>Puntos</th>
                                </tr>
                            </thead>
                            <tbody>
                                {sortedMovimientos.map((movimiento) => {
                                    const meta = MOVEMENT_META[movimiento.tipo_operacion] || {
                                        label: movimiento.tipo_operacion || 'Movimiento',
                                        title: 'Movimiento de puntos',
                                        Icon: History,
                                        className: 'neutral',
                                    };
                                    const Icon = meta.Icon;
                                    const amount = Number(movimiento.monto_puntos || 0);

                                    return (
                                        <tr key={movimiento.id}>
                                            <td>
                                                <span className={`${styles.typeBadge} ${styles[meta.className]}`}>
                                                    <Icon size={16} />
                                                    {meta.label}
                                                </span>
                                            </td>
                                            <td>
                                                <strong>{meta.title}</strong>
                                                <small>{movimiento.referencia || 'Sin referencia'}</small>
                                            </td>
                                            <td>{formatDate(movimiento.fecha)}</td>
                                            <td className={amount >= 0 ? styles.amountPositive : styles.amountNegative}>
                                                {amount > 0 ? '+' : ''}{amount.toLocaleString('es-BO')} pts
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <div className={styles.emptyState}>
                        <History size={34} />
                        <strong>Aún no tienes movimientos</strong>
                        <span>Cuando una compra sea entregada, verás aquí los puntos ganados.</span>
                    </div>
                )}
            </section>
        </AppView>
    );
};

export default MiBilleteraPuntos;
