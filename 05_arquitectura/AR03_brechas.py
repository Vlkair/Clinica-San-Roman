import pandas as pd

b = pd.DataFrame([
 # capa, elemento_actual, elemento_objetivo, tipo_brecha, esfuerzo, dependencias, origen
 ("Datos", "Paciente en 5 sistemas con 1,100 duplicados", "Maestro único de pacientes (MDM) con fuente autoritativa en HIS",
  "Modificar", "Alto", "—", "Principio dato único · Incidente G (34 exámenes erróneos)"),
 
 ("Datos", "Datos de salud sin cifrar en reposo", "Almacenamiento de historias clínicas cifrado (AES-256)",
  "Nuevo", "Medio", "—", "Sección 4.1 obligación Ley 29733 / ANPD · Riesgo H.1"),
 
 ("Aplicación", "Integración LIS-HIS por archivo plano manual", "Bus de interoperabilidad clínica en tiempo real (HL7/FHIR)",
  "Nuevo", "Alto", "Maestro único de pacientes", "Objetivo declarado de TI · Incidente G"),
 
 ("Aplicación", "Programación de camas y salas en hoja de cálculo", "Módulo de gestión de camas y quirófanos integrado al HIS",
  "Nuevo", "Medio", "Maestro único de pacientes", "Inventario de aplicaciones · Eliminación de Excel"),
 
 ("Aplicación", "Conciliación con aseguradoras en hoja de cálculo", "Módulo de liquidación y conciliación de aseguradoras en ERP/HIS",
  "Nuevo", "Medio", "—", "Inventario de aplicaciones · Eficiencia operacional"),
 
 ("Aplicación", "Citas del portal web se digitan a mano en HIS", "Integración API directa entre Portal de Citas y Agenda HIS",
  "Modificar", "Bajo", "Maestro único de pacientes", "Visión Sección 2.2 · Optimización de admisión"),
 
 ("Aplicación", "Sistema de planillas sin soporte y no integrado", "Módulo de gestión de personal y planillas integrado a contabilidad",
  "Reemplazar", "Medio", "—", "Inventario de aplicaciones · Obsoletización de software"),
 
 ("Tecnología", "Sala de máquinas con aire acondicionado doméstico", "Infraestructura resurgente / Cloud híbrida con respaldo inmutable",
  "Modificar", "Alto", "—", "Sección 4.3 DSS04 · Análisis BIA / Continuidad"),
 
 ("Tecnología", "Red LAN unificada (consultorios, administración y equipos)", "Segmentación de red por VLANs (Biomédica, Gestión, Wi-Fi)",
  "Modificar", "Bajo", "—", "Sección 4.1 Seguridad de la información"),
 
 ("Negocio", "Cuentas compartidas de médicos en consultorios", "Autenticación nominativa individual con MFA",
  "Modificar", "Bajo", "—", "Riesgo H.3 · Principio de protección de datos de salud"),
], columns=["capa", "actual", "objetivo", "tipo_brecha", "esfuerzo", "dependencias", "origen"])

# Guardar el CSV con los datos de Clínica San Ramón S.A.C.
b.to_csv("AR03_brechas.csv", index=False)

# Mostrar resúmenes en consola
print("=== RESUMEN POR CAPA Y TIPO DE BRECHA ===")
print(b.groupby(["capa", "tipo_brecha"]).size().to_string())
print(f"\nBrechas totales: {len(b)}")
print(f"Esfuerzo alto: {(b.esfuerzo=='Alto').sum()} | medio: {(b.esfuerzo=='Medio').sum()} | bajo: {(b.esfuerzo=='Bajo').sum()}")

# --- Paquetes de trabajo: agrupar brechas relacionadas ---
PAQUETES = {
 "PT-01 Gobierno de datos de salud": [
     "Paciente en 5 sistemas con 1,100 duplicados", 
     "Datos de salud sin cifrar en reposo"
 ],
 "PT-02 Interoperabilidad clínica (LIS-HIS-PACS)": [
     "Integración LIS-HIS por archivo plano manual", 
     "Citas del portal web se digitan a mano en HIS"
 ],
 "PT-03 Digitalización y control operacional (ERP/HIS)": [
     "Programación de camas y salas en hoja de cálculo", 
     "Conciliación con aseguradoras en hoja de cálculo", 
     "Sistema de planillas sin soporte y no integrado"
 ],
 "PT-04 Ciberseguridad y control de acceso nominativo": [
     "Red LAN unificada (consultorios, administración y equipos)", 
     "Cuentas compartidas de médicos en consultorios"
 ],
 "PT-05 Infraestructura resurgente y continuidad": [
     "Sala de máquinas con aire acondicionado doméstico"
 ],
}

print("\n=== PAQUETES DE TRABAJO (insumo del portafolio Sección 7) ===")
for p, items in PAQUETES.items():
    sub = b[b.actual.isin(items)]
    dep = ", ".join(sorted({d for d in sub.dependencias if d != "—"})) or "ninguna"
    print(f"{p}\n   brechas: {len(sub)} | esfuerzo máximo: "
          f"{sub.esfuerzo.map({'Bajo':1,'Medio':2,'Alto':3}).max()} | dependencias: {dep}")

# --- Secuencia derivada de las dependencias ---
print("\n=== SECUENCIA OBLIGADA POR DEPENDENCIAS ===")
print("  1. PT-01 Gobierno de datos de salud      (habilita PT-02 y PT-03)")
print("  2. PT-04 Ciberseguridad y accesos         (independiente, prioridad legal e inmediata)")
print("  3. PT-02 Interoperabilidad clínica       (depende de PT-01)")
print("  4. PT-03 Digitalización y ERP            (depende de PT-01)")
print("  5. PT-05 Infraestructura resurgente      (soporte continuo y renovaciones de TI)")
print("\n→ Esta secuencia condiciona la hoja de ruta (Sección 7.3).")
