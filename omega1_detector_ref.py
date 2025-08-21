# omega1_detector_ref.py
from dataclasses import dataclass
from typing import List, Tuple, Optional

Clause = Tuple[int, ...]
CNF = List[Clause]

@dataclass
class Omega1Result:
    is_omega1: bool
    witness_seed: Optional[int] = None
    witness_literal: Optional[int] = None
    witness_depth: Optional[int] = None
    conflict_kind: Optional[str] = None
    reasons: Optional[List[str]] = None
    witness_path: Optional[List[int]] = None

def read_dimacs(path: str) -> CNF:
    """Minimal DIMACS CNF loader. Lines end with a trailing 0."""
    F: CNF = []
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith(("c", "p")):
                continue
            nums = [int(x) for x in s.split() if x]
            if not nums:
                continue
            if nums[-1] != 0:
                raise ValueError("DIMACS clause line missing trailing 0")
            F.append(tuple(nums[:-1]))
    return F

def _has_empty_clause(F: CNF) -> bool:
    return any(len(c) == 0 for c in F)

def _simplify(F: CNF, lit: int):
    new_F: CNF = []
    for clause in F:
        if lit in clause:
            continue
        new_clause = tuple(x for x in clause if x != -lit)
        if len(new_clause) == 0:
            return new_F, True
        new_F.append(new_clause)
    return new_F, False

def _unit_propagate(F: CNF):
    path: List[int] = []
    depth = 0
    while True:
        units = [c[0] for c in F if len(c) == 1]
        if not units:
            return False, path, None, depth
        lit = units[0]
        path.append(lit)
        depth += 1
        F, made_empty = _simplify(F, lit)
        if made_empty:
            return True, path, lit, depth

def detect_omega1(F: CNF) -> Omega1Result:
    reasons: List[str] = []

    if _has_empty_clause(F):
        reasons.append("formula already contains an empty clause")
        return Omega1Result(
            is_omega1=True,
            witness_seed=None,
            witness_literal=None,
            witness_depth=0,
            conflict_kind="empty_clause",
            reasons=reasons,
            witness_path=[]
        )

    conflict, path, last_lit, depth = _unit_propagate([tuple(c) for c in F])
    if conflict:
        seed_var = abs(path[0]) if path else None
        reasons.append("unit propagation derives a contradiction (empty clause)")
        return Omega1Result(
            is_omega1=True,
            witness_seed=seed_var,
            witness_literal=last_lit,
            witness_depth=depth,
            conflict_kind="unit_conflict",
            reasons=reasons,
            witness_path=path
        )

    reasons.append("no contradiction found via unit propagation")
    return Omega1Result(is_omega1=False, reasons=reasons, witness_path=[])

# Fixtures for the “Run Fixtures” tab
def F_prime() -> CNF:
    return [(1,), (-1, 2), (1, -2)]

def F_doubleprime() -> CNF:
    return [(1, 2, 3), (-1, 2), (1, -2), (3, -1)]

def F_tripleprime() -> CNF:
    return [(1,), (2, 3), (-2, 3), (-3, 1)]

def F_hex() -> CNF:
    return [(1, 2), (3, 4), (5, -1), (-2, -3), (-4, -5), (1, -4)]
