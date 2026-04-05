#!/usr/bin/env node
/**
 * Script que carga variables del .env de la raíz del proyecto
 * Esto permite que frontend y backend lean del mismo .env centralizado
 * 
 * Uso: node scripts/load-env.js [comando]
 * Ejemplo: node scripts/load-env.js npm start
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Ruta al .env en la raíz del proyecto
const envPath = path.join(__dirname, '..', '.env');

// Leer .env
if (!fs.existsSync(envPath)) {
    console.error(`❌ .env no encontrado en: ${envPath}`);
    process.exit(1);
}

const envContent = fs.readFileSync(envPath, 'utf8');
const lines = envContent.split('\n');

// Procesar cada línea y cargar en process.env
lines.forEach(line => {
    // Ignorar comentarios y líneas vacías
    if (line.trim().startsWith('#') || !line.trim()) return;
    
    // Parsear KEY=VALUE
    const [key, ...valueParts] = line.split('=');
    if (!key) return;
    
    const cleanKey = key.trim();
    const value = valueParts.join('=').trim();
    
    // Si es REACT_APP_* o no está en process.env, agregarlo
    if (cleanKey.startsWith('REACT_APP_') || !process.env[cleanKey]) {
        process.env[cleanKey] = value;
    }
});

console.log(`✓ Variables de .env cargadas desde: ${envPath}`);

// Si hay argumentos adicionales, ejecutar comando
const args = process.argv.slice(2);
if (args.length > 0) {
    const [command, ...cmdArgs] = args;
    const child = spawn(command, cmdArgs, {
        env: process.env,
        stdio: 'inherit',
        shell: true
    });
    
    child.on('exit', (code) => {
        process.exit(code);
    });
} else {
    console.log('Variables disponibles:');
    Object.keys(process.env)
        .filter(key => key.startsWith('REACT_APP_') || key.startsWith('DJANGO_') || key.startsWith('DATABASE_'))
        .forEach(key => {
            console.log(`  ${key}=${process.env[key]}`);
        });
}
