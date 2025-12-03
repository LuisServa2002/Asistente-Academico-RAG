from typing import List, Dict, Tuple
import numpy as np
from collections import Counter
import re


class MetricasRAG:
    """
    Evaluación de métricas de recuperación y generación para sistema RAG
    """

    @staticmethod
    def precision_recall_f1(documentos_relevantes: List[str], documentos_recuperados: List[str]) -> Dict:
        """
        Calcula Precision, Recall y F1-score

        Args:
            documentos_relevantes: Documentos realmente relevantes
            documentos_recuperados: Documentos recuperados por el sistema

        Returns:
            Dict con precision, recall, f1-score
        """
        relevantes_set = set(documentos_relevantes)
        recuperados_set = set(documentos_recuperados)

        tp = len(relevantes_set & recuperados_set)
        fp = len(recuperados_set - relevantes_set)
        fn = len(relevantes_set - recuperados_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    @staticmethod
    def bleu_score(referencia: str, candidato: str, n_gramas: int = 4) -> float:
        """
        Calcula BLEU score (n-gramas coincidentes)

        Args:
            referencia: Texto de referencia
            candidato: Texto generado
            n_gramas: Tamaño de n-gramas (default 4)

        Returns:
            BLEU score entre 0 y 1
        """
        def obtener_ngramas(texto, n):
            palabras = texto.lower().split()
            return [tuple(palabras[i:i+n]) for i in range(len(palabras)-n+1)]

        ref_gramas = obtener_ngramas(referencia, n_gramas)
        cand_gramas = obtener_ngramas(candidato, n_gramas)

        if not ref_gramas or not cand_gramas:
            return 0.0

        coincidencias = sum((Counter(cand_gramas) & Counter(ref_gramas)).values())
        bleu = coincidencias / len(cand_gramas) if cand_gramas else 0.0

        return round(bleu, 4)

    @staticmethod
    def rouge_score(referencia: str, candidato: str) -> Dict:
        """
        Calcula ROUGE score (Recall-Oriented Understudy for Gisting Evaluation)
        Versión simplificada: ROUGE-1 y ROUGE-L

        Args:
            referencia: Texto de referencia
            candidato: Texto generado

        Returns:
            Dict con ROUGE-1 precision, recall, f1 y ROUGE-L
        """
        def obtener_tokens(texto):
            return texto.lower().split()

        ref_tokens = obtener_tokens(referencia)
        cand_tokens = obtener_tokens(candidato)

        # ROUGE-1: unigramas
        ref_counter = Counter(ref_tokens)
        cand_counter = Counter(cand_tokens)
        coincidencias = sum((cand_counter & ref_counter).values())

        rouge1_precision = coincidencias / len(cand_tokens) if cand_tokens else 0.0
        rouge1_recall = coincidencias / len(ref_tokens) if ref_tokens else 0.0
        rouge1_f1 = 2 * (rouge1_precision * rouge1_recall) / (rouge1_precision + rouge1_recall) if (rouge1_precision + rouge1_recall) > 0 else 0.0

        # ROUGE-L: subsecuencia común más larga
        lcs = MetricasRAG._longest_common_subsequence(ref_tokens, cand_tokens)
        rougeL_precision = len(lcs) / len(cand_tokens) if cand_tokens else 0.0
        rougeL_recall = len(lcs) / len(ref_tokens) if ref_tokens else 0.0
        rougeL_f1 = 2 * (rougeL_precision * rougeL_recall) / (rougeL_precision + rougeL_recall) if (rougeL_precision + rougeL_recall) > 0 else 0.0

        return {
            "rouge1": {
                "precision": round(rouge1_precision, 4),
                "recall": round(rouge1_recall, 4),
                "f1": round(rouge1_f1, 4),
            },
            "rougeL": {
                "precision": round(rougeL_precision, 4),
                "recall": round(rougeL_recall, 4),
                "f1": round(rougeL_f1, 4),
            },
        }

    @staticmethod
    def _longest_common_subsequence(seq1: List, seq2: List) -> List:
        """
        Calcula la subsecuencia común más larga
        """
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        # Reconstruir la LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                lcs.append(seq1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        return lcs[::-1]

    @staticmethod
    def similitud_coseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calcula similitud coseno entre dos vectores
        """
        if len(vec1) == 0 or len(vec2) == 0:
            return 0.0

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return round(float(dot_product / (norm1 * norm2)), 4)

    @staticmethod
    def evaluar_respuesta(
        referencia: str,
        candidato: str,
        documentos_relevantes: List[str] = None,
        documentos_recuperados: List[str] = None,
    ) -> Dict:
        """
        Evaluación completa de una respuesta

        Args:
            referencia: Respuesta de referencia
            candidato: Respuesta generada
            documentos_relevantes: Docs relevantes (opcional)
            documentos_recuperados: Docs recuperados (opcional)

        Returns:
            Dict con todas las métricas
        """
        metricas = {
            "bleu": MetricasRAG.bleu_score(referencia, candidato),
            "rouge": MetricasRAG.rouge_score(referencia, candidato),
        }

        if documentos_relevantes and documentos_recuperados:
            metricas["recuperacion"] = MetricasRAG.precision_recall_f1(
                documentos_relevantes, documentos_recuperados
            )

        return metricas
