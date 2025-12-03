from typing import List, Dict
import json
from pathlib import Path
from metricas import MetricasRAG


class EvaluadorRAG:
    """
    Herramienta para evaluar el sistema RAG con dataset de pruebas
    """

    def __init__(self, archivo_dataset: str = "dataset_evaluacion.json"):
        """
        Args:
            archivo_dataset: Archivo JSON con preguntas, respuestas y docs relevantes
        """
        self.archivo_dataset = archivo_dataset
        self.resultados = []
        self.metricas = MetricasRAG()

    def cargar_dataset(self) -> List[Dict]:
        """
        Carga dataset de evaluación
        Formato esperado:
        [
            {
                "pregunta": "¿Qué es RAG?",
                "respuesta_referencia": "RAG es...",
                "documentos_relevantes": ["doc1.pdf", "doc2.pdf"]
            }
        ]
        """
        try:
            with open(self.archivo_dataset, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Dataset no encontrado: {self.archivo_dataset}")
            return []

    def evaluar_pregunta(
        self,
        pregunta: str,
        respuesta_candidato: str,
        respuesta_referencia: str,
        documentos_recuperados: List[str],
        documentos_relevantes: List[str],
    ) -> Dict:
        """
        Evalúa una pregunta individual
        """
        evaluacion = {
            "pregunta": pregunta,
            "metricas": self.metricas.evaluar_respuesta(
                respuesta_referencia,
                respuesta_candidato,
                documentos_relevantes,
                documentos_recuperados,
            ),
        }
        self.resultados.append(evaluacion)
        return evaluacion

    def generar_reporte(self, archivo_salida: str = "reporte_evaluacion.json") -> Dict:
        """
        Genera reporte consolidado de evaluación
        """
        if not self.resultados:
            return {"error": "No hay resultados para reportar"}

        # Calcular promedios
        bleu_scores = [r["metricas"]["bleu"] for r in self.resultados if "bleu" in r["metricas"]]
        rouge1_f1 = [r["metricas"]["rouge"]["rouge1"]["f1"] for r in self.resultados if "rouge" in r["metricas"]]
        rougeL_f1 = [r["metricas"]["rouge"]["rougeL"]["f1"] for r in self.resultados if "rouge" in r["metricas"]]

        reporte = {
            "total_preguntas": len(self.resultados),
            "promedio_bleu": round(sum(bleu_scores) / len(bleu_scores), 4) if bleu_scores else 0.0,
            "promedio_rouge1_f1": round(sum(rouge1_f1) / len(rouge1_f1), 4) if rouge1_f1 else 0.0,
            "promedio_rougeL_f1": round(sum(rougeL_f1) / len(rougeL_f1), 4) if rougeL_f1 else 0.0,
            "resultados_detallados": self.resultados,
        }

        # Guardar reporte
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)

        return reporte

    def mostrar_resumen(self, reporte: Dict):
        """
        Muestra resumen de evaluación en consola
        """
        print("\n" + "="*60)
        print("REPORTE DE EVALUACIÓN DEL SISTEMA RAG")
        print("="*60)
        print(f"Total de preguntas evaluadas: {reporte['total_preguntas']}")
        print(f"Promedio BLEU: {reporte['promedio_bleu']}")
        print(f"Promedio ROUGE-1 F1: {reporte['promedio_rouge1_f1']}")
        print(f"Promedio ROUGE-L F1: {reporte['promedio_rougeL_f1']}")
        print("="*60 + "\n")
