"""Deterministic, heuristic checks over objects from a Speckle model."""

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuditResult:
    """Observed counts produced by the small set of local audit rules."""

    total_objects: int
    object_types: dict[str, int]
    structural_objects: int
    structural_objects_without_material: int
    objects_without_id: int
    duplicate_id_occurrences: int
    distinct_duplicate_ids: int


def _has_value(value: Any) -> bool:
    """Return whether a BIM property is present under simple empty-value rules."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (Mapping, list, tuple, set, frozenset)):
        return bool(value)
    return True


def _is_structural_type(type_name: str) -> bool:
    """Use a transparent name-based heuristic to identify common structure types."""
    normalized = type_name.casefold()
    return any(term in normalized for term in ("structure", "beam", "column", "wall"))


def audit_objects(objects: Iterable[Any]) -> AuditResult:
    """Count object types and run simple ID/material presence checks.

    This is not structural engineering analysis, a compliance assessment, or a
    predictive model. A structural object is identified only by the presence of
    one of the literal type-name terms in :func:`_is_structural_type`.
    """
    type_counts: Counter[str] = Counter()
    seen_ids: Counter[str] = Counter()
    total_objects = 0
    structural_objects = 0
    structural_objects_without_material = 0
    objects_without_id = 0

    for obj in objects:
        total_objects += 1
        raw_type = getattr(obj, "speckle_type", None)
        type_name = str(raw_type) if raw_type else type(obj).__name__
        type_counts[type_name] += 1

        raw_id = getattr(obj, "id", None)
        if raw_id is None or (isinstance(raw_id, str) and not raw_id.strip()):
            objects_without_id += 1
        else:
            seen_ids[str(raw_id)] += 1

        if _is_structural_type(type_name):
            structural_objects += 1
            if not _has_value(getattr(obj, "material", None)):
                structural_objects_without_material += 1

    duplicate_id_occurrences = sum(
        count - 1 for count in seen_ids.values() if count > 1
    )
    distinct_duplicate_ids = sum(1 for count in seen_ids.values() if count > 1)

    return AuditResult(
        total_objects=total_objects,
        object_types=dict(sorted(type_counts.items())),
        structural_objects=structural_objects,
        structural_objects_without_material=structural_objects_without_material,
        objects_without_id=objects_without_id,
        duplicate_id_occurrences=duplicate_id_occurrences,
        distinct_duplicate_ids=distinct_duplicate_ids,
    )


def format_audit_summary(result: AuditResult) -> str:
    """Format an aggregate summary without exposing model object identifiers."""
    lines = [
        "Auditoria heurística local — contagens observadas, sem nota de conformidade.",
        f"Objetos percorridos: {result.total_objects}",
        f"Tipos de objeto encontrados: {len(result.object_types)}",
        "Objetos estruturais identificados pela heurística: "
        f"{result.structural_objects}",
    ]

    if result.structural_objects:
        lines.append(
            "Objetos estruturais sem propriedade 'material': "
            f"{result.structural_objects_without_material} de "
            f"{result.structural_objects}"
        )
    else:
        lines.append(
            "Objetos estruturais sem propriedade 'material': não avaliado "
            "(nenhum tipo reconhecido pela heurística)"
        )

    lines.extend(
        [
            f"Objetos sem ID preenchido: {result.objects_without_id}",
            "Ocorrências excedentes de IDs repetidos: "
            f"{result.duplicate_id_occurrences}",
            f"Valores de ID repetidos distintos: {result.distinct_duplicate_ids}",
            "",
            "Distribuição por tipo:",
        ]
    )
    lines.extend(
        f"- {type_name}: {count}" for type_name, count in result.object_types.items()
    )
    lines.extend(
        [
            "",
            "Limites: regras simples de presença e nomes de tipo; não verifica "
            "cálculos estruturais, normas, conformidade, causalidade ou risco. "
            "A identificação de tipos estruturais é heurística.",
        ]
    )
    return "\n".join(lines)
