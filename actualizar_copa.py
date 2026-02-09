#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar la Copa de la Domiciliación desde un archivo CSV
"""

import csv
import re
import sys

def leer_csv(archivo_csv):
    """Lee el archivo CSV y retorna una lista de asesores"""
    asesores = []
    
    # Intentar diferentes codificaciones
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(archivo_csv, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
                # Verificar si hay contenido
                if not content.strip():
                    continue
                
                # Volver al inicio del archivo
                file.seek(0)
                
                # Leer CSV
                reader = csv.DictReader(file)
                temp_asesores = []
                
                for row in reader:
                    # Obtener valores con diferentes variaciones de nombres de columna
                    nombre = (row.get('Nombre') or row.get('nombre') or row.get('NOMBRE') or '').strip()
                    domiciliaciones_str = (row.get('Domiciliaciones') or row.get('domiciliaciones') or row.get('DOMICILIACIONES') or '0').strip()
                    area = (row.get('Area') or row.get('area') or row.get('AREA') or row.get('Área') or 'Sin área').strip()
                    
                    # Convertir domiciliaciones a número
                    try:
                        domiciliaciones = int(domiciliaciones_str)
                    except:
                        domiciliaciones = 0
                    
                    if nombre:
                        temp_asesores.append({
                            'nombre': nombre,
                            'domiciliaciones': domiciliaciones,
                            'area': area if area else 'Sin área'
                        })
                
                if temp_asesores:
                    print(f"✅ Archivo leído correctamente con codificación: {encoding}")
                    print(f"📊 Total de asesores encontrados: {len(temp_asesores)}")
                    asesores = temp_asesores
                    return asesores
                    
        except Exception as e:
            continue
    
    if not asesores:
        print("❌ Error: No se pudieron leer datos del archivo CSV")
        print("Verifica que:")
        print("  1. El archivo 'datos.csv' existe en la misma carpeta")
        print("  2. Tiene las columnas: Nombre, Domiciliaciones, Area")
        print("  3. Tiene al menos una fila de datos")
        sys.exit(1)
    
    return asesores

def generar_javascript(asesores):
    """Genera el código JavaScript con los datos de asesores"""
    js_code = "        const datosAsesores = [\n"
    
    for asesor in asesores:
        nombre = asesor['nombre'].replace('"', '\\"')  # Escapar comillas
        area = asesor['area'].replace('"', '\\"')
        js_code += f'            {{nombre: "{nombre}", domiciliaciones: {asesor["domiciliaciones"]}, area: "{area}"}},\n'
    
    js_code += "        ];"
    return js_code

def actualizar_html(archivo_html, asesores):
    """Actualiza el archivo HTML con los nuevos datos"""
    try:
        with open(archivo_html, 'r', encoding='utf-8') as file:
            contenido = file.read()
    except:
        print(f"❌ Error: No se encontró el archivo '{archivo_html}'")
        print(f"Asegúrate de que está en la misma carpeta que este script")
        sys.exit(1)
    
    # Generar nuevo código JavaScript
    nuevo_js = generar_javascript(asesores)
    
    # Patrón para encontrar la sección de datos
    patron = r'        const datosAsesores = \[.*?\];'
    
    # Verificar que el patrón existe
    if not re.search(patron, contenido, flags=re.DOTALL):
        print("❌ Error: No se encontró la sección de datos en el HTML")
        print("Verifica que estás usando el archivo correcto")
        sys.exit(1)
    
    # Reemplazar los datos
    contenido_actualizado = re.sub(patron, nuevo_js, contenido, flags=re.DOTALL)
    
    # Guardar el archivo actualizado
    with open(archivo_html, 'w', encoding='utf-8') as file:
        file.write(contenido_actualizado)
    
    print(f"\n✅ ¡Archivo HTML actualizado exitosamente!")
    print(f"📊 Total de asesores: {len(asesores)}")
    print(f"📈 Total de domiciliaciones: {sum(a['domiciliaciones'] for a in asesores)}")
    
    # Mostrar TOP 5
    asesores_ordenados = sorted(asesores, key=lambda x: x['domiciliaciones'], reverse=True)
    print(f"\n🏆 TOP 5 Asesores:")
    for i, asesor in enumerate(asesores_ordenados[:5], 1):
        print(f"  {i}. {asesor['nombre']} - {asesor['domiciliaciones']} domiciliaciones ({asesor['area']})")

def main():
    """Función principal"""
    print("🏆 Copa de la Domiciliación 2026 - Actualizador")
    print("=" * 50)
    
    archivo_csv = "datos.csv"
    archivo_html = "copa_dashboard_optimizado.html"
    
    # Leer datos del CSV
    print(f"📂 Leyendo datos de: {archivo_csv}")
    asesores = leer_csv(archivo_csv)
    
    # Actualizar HTML
    print(f"🔄 Actualizando archivo: {archivo_html}")
    actualizar_html(archivo_html, asesores)
    
    print("\n✨ ¡Listo! Ahora puedes abrir el archivo HTML en tu navegador")
    print("📁 Archivo actualizado: copa_dashboard_optimizado.html")

if __name__ == "__main__":
    main()