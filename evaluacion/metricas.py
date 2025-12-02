import json
import time
from typing import Dict, List

import numpy as np
from rouge_score import rouge_scorer


class EvaluadorAsistente:
    """
    Sistema de evaluación para el asistente académico RAG
    """

    def __init__(self, asistente):
        """
        Args:
            asistente: Instancia de AsistenteAcademico
        """
        self.asistente = asistente
        self.scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"], use_stemmer=True
        )
        self.resultados = []

    def cargar_conjunto_prueba(self, ruta_json: str):
        """
        Carga preguntas de prueba desde JSON

        Formato esperado:
        [
            {
                "pregunta": "¿Qué es RAG?",
                "respuesta_esperada": "RAG es Retrieval-Augmented Generation...",
                "categoria": "conceptual"
            },
            ...
        ]
        """
        with open(ruta_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluar_retrieval(
        self, pregunta: str, fragmentos_relevantes: List[str]
    ) -> Dict:
        """
        Evalúa la calidad del sistema de recuperación

        Args:
            pregunta: Pregunta realizada
            fragmentos_relevantes: IDs o textos de fragmentos que deberían recuperarse

        Returns:
            Métricas de precisión, recall, F1
        """
        resultado = self.asistente.consultar(pregunta)
        fragmentos_recuperados = resultado["fuentes"]

        # Convertir a conjunto para comparación
        recuperados_texto = {doc.page_content for doc in fragmentos_recuperados}
        relevantes_texto = set(fragmentos_relevantes)

        # Calcular métricas
        tp = len(recuperados_texto.intersection(relevantes_texto))
        fp = len(recuperados_texto - relevantes_texto)
        fn = len(relevantes_texto - recuperados_texto)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "fragmentos_recuperados": len(fragmentos_recuperados),
            "fragmentos_relevantes": len(fragmentos_relevantes),
        }

    def evaluar_generacion(
        self, respuesta_generada: str, respuesta_referencia: str
    ) -> Dict:
        """
        Evalúa la calidad de la respuesta generada usando ROUGE

        Args:
            respuesta_generada: Respuesta del modelo
            respuesta_referencia: Respuesta ideal/esperada

        Returns:
            Scores ROUGE
        """
        scores = self.scorer.score(respuesta_referencia, respuesta_generada)

        return {
            "rouge1_f1": scores["rouge1"].fmeasure,
            "rouge2_f1": scores["rouge2"].fmeasure,
            "rougeL_f1": scores["rougeL"].fmeasure,
        }

    def evaluar_latencia(self, pregunta: str) -> float:
        """
        Mide el tiempo de respuesta

        Returns:
            Tiempo en segundos
        """
        inicio = time.time()
        self.asistente.consultar(pregunta)
        fin = time.time()

        return fin - inicio

    def evaluar_conjunto_completo(self, conjunto_prueba: List[Dict]) -> Dict:
        """
        Evalúa el asistente con un conjunto completo de pruebas

        Args:
            conjunto_prueba: Lista de diccionarios con preguntas y respuestas esperadas

        Returns:
            Resultados agregados
        """
        print(f"\n🧪 Evaluando {len(conjunto_prueba)} preguntas...\n")

        metricas_rouge = []
        tiempos = []
        respuestas_completas = []

        for i, item in enumerate(conjunto_prueba, 1):
            pregunta = item["pregunta"]
            respuesta_esperada = item.get("respuesta_esperada", "")

            print(f"[{i}/{len(conjunto_prueba)}] {pregunta[:50]}...")

            # Medir latencia
            tiempo = self.evaluar_latencia(pregunta)
            tiempos.append(tiempo)

            # Obtener respuesta
            resultado = self.asistente.consultar(pregunta)
            respuesta = resultado["respuesta"]

            # Evaluar con ROUGE si hay respuesta esperada
            if respuesta_esperada:
                rouge = self.evaluar_generacion(respuesta, respuesta_esperada)
                metricas_rouge.append(rouge)

            respuestas_completas.append(
                {
                    "pregunta": pregunta,
                    "respuesta_generada": respuesta,
                    "respuesta_esperada": respuesta_esperada,
                    "tiempo_respuesta": tiempo,
                    "num_fuentes": len(resultado["fuentes"]),
                }
            )

        # Calcular promedios
        resultados = {
            "total_preguntas": len(conjunto_prueba),
            "tiempo_promedio": np.mean(tiempos),
            "tiempo_min": np.min(tiempos),
            "tiempo_max": np.max(tiempos),
        }

        if metricas_rouge:
            resultados["rouge1_promedio"] = np.mean(
                [m["rouge1_f1"] for m in metricas_rouge]
            )
            resultados["rouge2_promedio"] = np.mean(
                [m["rouge2_f1"] for m in metricas_rouge]
            )
            resultados["rougeL_promedio"] = np.mean(
                [m["rougeL_f1"] for m in metricas_rouge]
            )

        resultados["respuestas_detalladas"] = respuestas_completas

        return resultados

    def evaluar_manual(self, preguntas: List[str]) -> None:
        """
        Evaluación manual interactiva

        Args:
            preguntas: Lista de preguntas a evaluar
        """
        print("\n📋 Evaluación Manual")
        print("Califica cada respuesta de 1 a 5:\n")

        evaluaciones = []

        for pregunta in preguntas:
            print(f"\n{'=' * 60}")
            print(f"❓ {pregunta}")
            print("=" * 60)

            resultado = self.asistente.consultar(pregunta)
            print(f"\n💬 Respuesta:\n{resultado['respuesta']}")

            if resultado["fuentes"]:
                print(f"\n📌 {len(resultado['fuentes'])} fuentes utilizadas")

            # Solicitar calificación
            relevancia = int(input("\nRelevancia (1-5): "))
            coherencia = int(input("Coherencia (1-5): "))
            precision = int(input("Precisión (1-5): "))

            evaluaciones.append(
                {
                    "pregunta": pregunta,
                    "relevancia": relevancia,
                    "coherencia": coherencia,
                    "precision": precision,
                    "promedio": (relevancia + coherencia + precision) / 3,
                }
            )

        # Mostrar resumen
        print(f"\n{'=' * 60}")
        print("📊 RESUMEN DE EVALUACIÓN MANUAL")
        print("=" * 60)

        promedio_relevancia = np.mean([e["relevancia"] for e in evaluaciones])
        promedio_coherencia = np.mean([e["coherencia"] for e in evaluaciones])
        promedio_precision = np.mean([e["precision"] for e in evaluaciones])
        promedio_general = np.mean([e["promedio"] for e in evaluaciones])

        print(f"Relevancia promedio:  {promedio_relevancia:.2f}/5")
        print(f"Coherencia promedio:  {promedio_coherencia:.2f}/5")
        print(f"Precisión promedio:   {promedio_precision:.2f}/5")
        print(f"Calificación general: {promedio_general:.2f}/5")

        return evaluaciones

    def generar_reporte(
        self, resultados: Dict, ruta_salida: str = "reporte_evaluacion.json"
    ):
        """
        Genera un reporte JSON con los resultados
        """
        with open(ruta_salida, "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Reporte guardado en: {ruta_salida}")


# ========== EJEMPLO DE USO ==========

if __name__ == "__main__":
    # from asistente import AsistenteAcademico

    # # Inicializar asistente
    # asistente = AsistenteAcademico()
    # asistente.cargar_vectorstore_existente()

    # # Crear evaluador
    # evaluador = EvaluadorAsistente(asistente)

    # Conjunto de prueba ejemplo
    conjunto_prueba = [
        {
            "pregunta": "¿Qué es RAG?",
            "respuesta_esperada": "RAG (Retrieval-Augmented Generation) es una técnica que combina recuperación de información con generación de lenguaje natural para producir respuestas fundamentadas en documentos.",
            "categoria": "conceptual",
        },
        {
            "pregunta": "¿Cuáles son los objetivos específicos del proyecto?",
            "respuesta_esperada": "Los objetivos incluyen implementar NLP, integrar búsqueda vectorial, desarrollar un modelo RAG, evaluar el rendimiento y analizar implicaciones éticas.",
            "categoria": "proyecto",
        },
        {
            "pregunta": "¿Qué herramientas se utilizarán para la implementación?",
            "respuesta_esperada": "Se utilizarán LangChain, FAISS o ChromaDB para almacenamiento vectorial, Streamlit para la interfaz y modelos de embeddings como Sentence-BERT.",
            "categoria": "técnico",
        },
    ]

    # Evaluar
    # resultados = evaluador.evaluar_conjunto_completo(conjunto_prueba)
    # evaluador.generar_reporte(resultados)

    # Evaluación manual opcional
    # preguntas_manual = [
    #     "¿Cómo funciona la búsqueda vectorial?",
    #     "¿Qué consideraciones éticas tiene el proyecto?"
    # ]
    # evaluador.evaluar_manual(preguntas_manual)

    print("\n✅ Script de evaluación listo para usar")
