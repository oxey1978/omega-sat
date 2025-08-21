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
    """Very small DIMACS CNF loader."""
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

def detect_omega1(F: CNF) -> Omega1Result:
    """Placeholder — replace with your real Ω1 detector later."""
    return Omega1Result(
        is_omega1=False,
        reasons=["placeholder Ω1 detector — replace with real implementation"]
    )

# Tiny fixture generators (toy CNFs)
def F_prime() -> CNF:
    return [(1, 2), (-1, 2), (1, -2)]

def F_doubleprime() -> CNF:
    return [(1, 2, 3), (-1, 2), (1, -2), (3, -1)]

def F_tripleprime() -> CNF:
    return [(1,), (2, 3), (-2, 3), (-3, 1)]

def F_hex() -> CNF:
    return [(1, 2), (3, 4), (5, -1), (-2, -3), (-4, -5), (1, -4)]
