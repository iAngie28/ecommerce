import React, { useState } from 'react';
import { BarChart3, Database, Mic, Settings2 } from 'lucide-react';
import AppView from 'shared/widgets/AppView/AppView';
import VoiceQueryWidget from '../components/VoiceQueryWidget';
import ReportesEstaticos from '../components/ReportesEstaticos';
import ReporteDinamicoBuilder from '../components/ReporteDinamicoBuilder';
import styles from './ReportesView.module.css';

export default function ReportesView() {
  const [activeTab, setActiveTab] = useState('estaticos');

  return (
    <AppView title="Reportes & Análisis" subtitle="Inteligencia de negocio y predicciones con IA.">
      <div className={styles.tabsContainer}>
        <div className={styles.tabList}>
          <button 
            className={`${styles.tab} ${activeTab === 'estaticos' ? styles.activeTab : ''}`}
            onClick={() => setActiveTab('estaticos')}
          >
            <BarChart3 size={18} /> Reportes Básicos
          </button>
          <button 
            className={`${styles.tab} ${activeTab === 'dinamicos' ? styles.activeTab : ''}`}
            onClick={() => setActiveTab('dinamicos')}
          >
            <Settings2 size={18} /> Reportes Dinámicos
          </button>
          <button 
            className={`${styles.tab} ${activeTab === 'voz' ? styles.activeTab : ''}`}
            onClick={() => setActiveTab('voz')}
          >
            <Mic size={18} /> Asistente IA por Voz
          </button>
        </div>

        <div className={styles.tabContent}>
          {activeTab === 'estaticos' && <ReportesEstaticos />}
          {activeTab === 'dinamicos' && <ReporteDinamicoBuilder />}
          {activeTab === 'voz' && <VoiceQueryWidget />}
        </div>
      </div>
    </AppView>
  );
}
