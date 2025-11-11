# Simulación de Adaptación Muscular (Proyecto Final — Modelación y Simulación)

> **Resumen:** Implementamos un modelo de **Dinámica de Sistemas** con analogía **SEIR** y **retrasos tipo Erlang** para estudiar la **adaptación muscular** en atletas bajo distintas **intervenciones** (bloques de entrenamiento, deload, adherencia, proteína, sueño). Incluimos **métricas cuantitativas**, **análisis de sensibilidad** y materiales para **informe + presentación**. El proyecto está alineado con los contenidos del curso (retrasos/retroalimentación, SIR/SEIR, ABM/heterogeneidad/redes, espacio de estados/estabilidad, DES e híbridos).

---

## 🎯 Objetivos de aprendizaje
- Relacionar **estructura → dinámica** (retrasos y lazos de retroalimentación) con comportamientos observados.
- Comparar **SEIR con retraso** vs **SIR (sin retraso)** y explicar diferencias.
- Evaluar intervenciones: **deload**, **adherencia**, **microlesión** (φ↑) y **estancamiento** (β↓).
- Reportar **métricas** (picos, ΔM, AUC) y realizar **sensibilidad** de parámetros.
---

## 🧠 Modelo (resumen)
- Estados: **S** (susceptible a mejorar), **E(1..k)** (exposición con **retraso**), **I** (estimulado/fatigado), **R** (adaptado).
- Transiciones: \(\lambda(t)=\beta\,A(t)\), cadena **Erlang** (k etapas con parámetro \(\alpha\)), recuperación \(\gamma\) y recaída \(\phi\).
- Stock agregado **M(t)** (masa/rendimiento) con ganancia por **R** y pérdida hacia el baseline.
- **Intervenciones**: bloques *hipertrofia→fuerza→deload*; adherencia, proteína y sueño modifican **A(t)**; deload afecta **\(\gamma,\phi\)**.
- Extensiones incluidas: **microlesión** (pulso de \(\phi\)), **estancamiento** (decaimiento efectivo en \(\beta\)).

---

## 📦 Estructura del repositorio
```
src/
  sd_model/
    __init__.py
    params.py                # parámetros por defecto
    seir_muscle.py           # ODEs + RK4 (SEIR con retrasos + lazo de fatiga)
    interventions.py         # A(t), deload, microlesión, estancamiento
    experiments.py           # corridas base, métricas, sensibilidad, toggles
    run_all.py               # runner headless para exportar figuras/tablas
  abm/
    model.py                
notebooks/
  01_validacion_sd.ipynb     # validación y con/sin retraso (con path-fix)
  02_experimentos_sd.ipynb   # adherencia y deload
  03_metricas_sensibilidad.ipynb  # métricas + heatmap + fase I–R
  04_experimentos_finales.ipynb   # exporta figuras y tablas
reports/
  informe_plantilla.md       # plantilla del informe
  figs/                      # figuras exportadas
  tables/                    # tablas CSV exportadas
slides/
  presentacion_outline.md    # guion de 6–10 láminas
data/
  athletes_cohort_500.csv    # cohorte sintética (500 filas, con referencias)
  synthetic_profiles.csv     # placeholder mínimo
requirements.txt
```

---

## ⚙️ Requisitos
- Python **3.10+**
- Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo correr (dos opciones)

### Opción A — Runner (sin abrir notebooks)
Genera **todas** las figuras y tablas en `reports/`:
```bash
python -m sd_model.run_all
```
**Salidas principales:**
- `reports/figs/` → `A_R_contra_sin_retraso.png`, `B_M_deload_on_off.png`, `C_M_adherencia.png`, `D_M_microlesion_estancamiento.png`, `E_heatmap_beta_phi.png`
- `reports/tables/` → `B_metricas_deload.csv`, `C_metricas_adherencia.csv`

### Opción B — Notebooks (con path‑fix incluido)
1. Abrí `notebooks/01_validacion_sd.ipynb` y ejecutá todo.  
2. Continuá con `02_`, `03_` y `04_` para obtener la batería completa de resultados.
> Los notebooks ya agregan `../src` al `sys.path` automáticamente.

---

## 🧪 Experimentos incluidos
- **A. SEIR (con retraso) vs SIR (sin retraso)** — impacto del retraso en el perfil de **R(t)** y **M(t)**.
- **B. Deload ON/OFF** — efecto en picos y masa final (**ΔM_final**, **AUC_I**).
- **C. Adherencia alta vs baja** — escenarios con `A(t)` constante para comparar sensibilidad al cumplimiento.
- **D. Microlesión vs Estancamiento** — pulso en **φ** y decaimiento en **β**.
- **E. Sensibilidad** — heatmap de **M(T)** barriendo **β** y **φ**.

**Métricas reportadas:** `t_peak_R`, `peak_R`, `t_peak_M`, `peak_M`, `ΔM_final`, `AUC_I`.

---

## 🗂️ Dataset sintético (500 filas)
Archivo: `data/athletes_cohort_500.csv`  
Columnas: `experience`, `goal`, `sleep_hours`, `protein_gkg`, `adherence`, `health`, banderas `adequate_protein`, `sleep_ok`.



## ✅ Qué cumple ya
- [x] **Tema/Problema/Modelo/Simulación** (Task 1)
- [x] **Implementación** modular + reproducible (Task 2)
- [x] **Análisis** con métricas, sensibilidad y fase (Task 3)
- [x] **Conclusiones & materiales** (plantilla informe + guion slides) (Task 4)
- [x] Fix de rutas en notebooks (portables entre equipos)
- [x] Runner para generación automática de resultados
- [x] Dataset sintético (500 filas) con variables útiles para segmentación


## 🗒️ Buenas prácticas
- Documentar los cambios de parámetros al correr escenarios.
- Guardar las semillas aleatorias para reproducibilidad.
- Incluir en el informe: supuestos, límites y amenazas a la validez.

---

## 👥 Colaboración
- Abrir issues/PRs por feature (p. ej., `feature/segmentos-cohorte`).
- Convención de commits: `feat:`, `fix:`, `docs:`, `refactor:`.

---

## 📚 Referencias (para el informe)
- Apuntes del curso: **retrasos & retroalimentación**, **SIR/SEIR**, **ABM/heterogeneidad/redes**, **estado‑espacio**, **DES/híbridos**.
- Recomendaciones generales de proteína para poblaciones activas, guías de sueño para adultos y adherencia a programas de ejercicio (ver bibliografía en el informe).

---

> Si algo no corre igual en las máquinas del equipo, usar la **Opción A (runner)**. Los notebooks ya traen el **path‑fix**, pero cualquier duda: revisar la celda inicial que añade `../src` al `sys.path`.
