import React, { useState } from 'react';
import styles from '../../styles/Predicciones.module.css';
import { generatePDF, generateExcel } from 'utils/exports/exportOrchestrator';
import { Button } from 'shared/components';
import { FileText, Table } from 'lucide-react';

export default function ExportButtons({ data, prediccionConfig }) {
  const [exportingExcel, setExportingExcel] = useState(false);
  const [exportingPDF, setExportingPDF] = useState(false);

  const handleDownloadExcel = async () => {
    if (!data || !data.predicciones) return;
    setExportingExcel(true);
    try {
      const title = `Predicción ${prediccionConfig?.tipo === 'ventas_totales' ? 'Global' : (prediccionConfig?.tipo || '')}`;
      await generateExcel('prediccion', data, { 
        title: title
      });
    } finally {
      setExportingExcel(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!data || !data.predicciones) return;
    setExportingPDF(true);
    try {
      const title = `Predicción ${prediccionConfig?.tipo === 'ventas_totales' ? 'Global' : (prediccionConfig?.tipo || '')}`;
      await generatePDF('prediccion', data, { 
        title: title
      });
    } finally {
      setExportingPDF(false);
    }
  };

  return (
    <div className={styles.exportButtons} style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
      <Button 
        variant="danger"
        onClick={handleDownloadPDF}
        disabled={exportingPDF || exportingExcel}
        leftIcon={<FileText size={18} />}
      >
        {exportingPDF ? 'Exportando...' : 'PDF'}
      </Button>
      
      <Button 
        variant="success"
        onClick={handleDownloadExcel}
        disabled={exportingExcel || exportingPDF}
        leftIcon={<Table size={18} />}
      >
        {exportingExcel ? 'Exportando...' : 'Excel'}
      </Button>
    </div>
  );
}
