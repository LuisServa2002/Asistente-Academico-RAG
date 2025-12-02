# Plan de Emergencia - Última Semana 🚨

## Situación Actual
- **Tiempo disponible**: ~5-7 días
- **Código completado**: 70%
- **Estado**: Módulos implementados pero NO integrados ni probados
- **Riesgo**: Alto - necesitan demo funcional para el examen

---

## 🎯 Objetivo Mínimo Viable (MVP)

**Tener un sistema funcional que:**
1. Cargue PDFs académicos
2. Responda preguntas sobre esos PDFs
3. Muestre fuentes citadas
4. Tenga métricas de evaluación documentadas

---

## 📅 Cronograma de Emergencia (5 días)

### **DÍA 1: Hacer que funcione** ⚡ CRÍTICO
**Objetivo**: Sistema corriendo end-to-end

#### Mañana (3-4 horas)
- [ ] Verificar que Ollama esté instalado y corriendo
- [ ] Descargar modelo: `ollama pull llama2:7b`
- [ ] Actualizar `requirements.txt` a versiones compatibles
- [ ] Instalar dependencias: `pip install -r requirements.txt`

#### Tarde (3-4 horas)
- [ ] Arreglar imports deprecados en `asistente.py`
- [ ] Descomentar integración en `app.py`
- [ ] Probar `asistente.py` standalone con 1 PDF simple
- [ ] Si funciona, probar interfaz Streamlit completa

**Entregable Día 1**: Sistema funcionando localmente, aunque sea con 1 PDF

---

### **DÍA 2: Preparar datos y evaluar** 📊
**Objetivo**: Tener evidencia de que funciona

#### Mañana (2-3 horas)
- [ ] Conseguir 2-3 PDFs académicos relevantes (IA, ML, etc.)
- [ ] Cargarlos en el sistema
- [ ] Hacer 10-15 preguntas de prueba manualmente
- [ ] Capturar screenshots de respuestas buenas

#### Tarde (3-4 horas)
- [ ] Crear `evaluacion/test_preguntas.json` (mínimo 5 preguntas)
- [ ] Ejecutar `metricas.py` para obtener métricas automáticas
- [ ] Documentar resultados (ROUGE, latencia, etc.)
- [ ] Hacer evaluación manual de calidad

**Entregable Día 2**: Dataset de pruebas + métricas documentadas

---

### **DÍA 3: Documentación técnica** 📝
**Objetivo**: Informe y README listo

#### Mañana (3 horas)
- [ ] Crear `README.md` con:
  - Instrucciones de instalación
  - Cómo usar el sistema
  - Ejemplos de consultas
- [ ] Documentar estructura del proyecto
- [ ] Crear `.gitignore` apropiado

#### Tarde (4 horas)
- [ ] Redactar informe técnico final:
  - Introducción y objetivos
  - Arquitectura implementada
  - Resultados de evaluación
  - Limitaciones y trabajo futuro

**Entregable Día 3**: README + Informe técnico borrador

---

### **DÍA 4: Análisis ético y presentación** 🎤
**Objetivo**: Completar aspectos éticos y actualizar slides

#### Mañana (2-3 horas)
- [ ] Implementar disclaimers en la UI
- [ ] Agregar sistema de citación de fuentes (ya está parcialmente)
- [ ] Documentar limitaciones conocidas
- [ ] Análisis de posibles sesgos

#### Tarde (3-4 horas)
- [ ] Actualizar `Presentación.pdf` con:
  - Resultados reales (screenshots)
  - Métricas obtenidas
  - Demostración del sistema
- [ ] Preparar video/GIF de demostración (opcional pero recomendado)

**Entregable Día 4**: Sección ética + Presentación actualizada

---

### **DÍA 5: Pulir y preparar entrega** ✨
**Objetivo**: Refinamiento y backup

#### Mañana (2-3 horas)
- [ ] Revisar y corregir informe técnico
- [ ] Verificar que todos los screenshots/evidencias estén incluidos
- [ ] Probar instalación desde cero (en otra máquina si es posible)
- [ ] Crear video de demostración de 2-3 minutos

#### Tarde (2-3 horas)
- [ ] Ensayar presentación oral
- [ ] Preparar respuestas a preguntas típicas:
  - ¿Por qué LLaMA y no GPT?
  - ¿Cómo funciona RAG?
  - ¿Qué métricas obtuvieron?
- [ ] Backup del proyecto completo
- [ ] Subir a GitHub (si aplica)

**Entregable Día 5**: Proyecto completo listo para entregar/presentar

---

## 🔥 Divisón de Trabajo Sugerida (5 personas)

| Persona | Días 1-2 | Días 3-4 | Día 5 |
|---------|----------|----------|-------|
| **Luis / Diego P.** | Integración técnica (hacer funcionar) | README + documentación | Testing final |
| **Melissa / Diego O.** | Preparar PDFs + ejecutar pruebas | Análisis ético + disclaimers | Video demo |
| **Gonzalo** | Crear dataset + métricas | Informe técnico + presentación | Ensayo presentación |

**Todos**: Día 5 tarde - Ensayo grupal de la presentación

---

## ⚠️ Plan B (si algo falla)

### Si Ollama no funciona en alguna laptop:
1. **Opción A**: Usar Google Colab con GPU gratuita
2. **Opción B**: Un miembro ejecuta el sistema y comparte screenshots/resultados
3. **Opción C**: Usar Groq API (gratuita) como alternativa rápida

### Si los embeddings tardan mucho:
1. Usar PDFs pequeños (10-20 páginas máximo)
2. Reducir chunk_size a 500
3. Procesar solo 1-2 PDFs para la demo

### Si no hay tiempo para evaluación completa:
1. Evaluación manual mínima (5 preguntas)
2. Documentar al menos latencia y satisfacción subjetiva
3. Ser honestos sobre limitaciones del tiempo

---

## 📋 Checklist Mínimo para Aprobar

- [ ] Sistema funciona y responde preguntas
- [ ] Al menos 1 PDF académico procesado
- [ ] Screenshots de 3-5 consultas exitosas
- [ ] README con instrucciones
- [ ] Informe técnico (aunque sea corto)
- [ ] Presentación actualizada con resultados reales
- [ ] Análisis ético básico documentado

---

## 💡 Consejos Finales

1. **Priorizar FUNCIONALIDAD sobre PERFECCIÓN**
2. **Documentar TODO lo que hagan** (screenshots, errores, soluciones)
3. **Comunicación diaria del equipo** (WhatsApp/Discord)
4. **No reimplementar todo**: el código está bueno, solo intégrenlo
5. **Tener un Plan B** para la demo si algo falla

---

## 🎯 Próximo Paso INMEDIATO

**Acción #1**: Verificar que Ollama esté instalado
```bash
ollama --version
ollama list
ollama pull llama2:7b
```

**Acción #2**: Probar `asistente.py` standalone
```bash
python asistente.py
```

Si estas dos cosas funcionan, están a 1 día de tener el sistema completo funcionando.

**¿Por dónde empezamos?**
