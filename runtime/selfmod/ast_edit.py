"""AST-located source edits for cognition/mutable modules (protected).

Each transform parses the module, locates its target node with ``ast`` and splices
the new text at that node's exact source span, so comments and layout elsewhere are
preserved. Every result is re-parsed; a transform that cannot locate its target
raises ``EditError`` (recorded as a rejected proposal, never silently skipped).

Transforms
  const_scale(name, factor)      NAME = c        ->  NAME = c * factor
  const_add(name, delta)         NAME = c        ->  NAME = c + delta
  const_set(name, value)         NAME = c        ->  NAME = value
  swap_call(func, old, new)      old(...) in func ->  new(...)
  insert_term(func, arg, coef)   return e         ->  return e + TERM_<FUNC>_<ARG> * arg
                                 (+ new module constant TERM_<FUNC>_<ARG> = coef)
  reorder(func, index)           swap statements index, index+1 of func's body
"""

from __future__ import annotations

import ast
import difflib
from typing import Any, Dict, List, Tuple


class EditError(ValueError):
    pass


def fmt_number(v: float) -> str:
    s = f"{float(v):.6g}"
    if not any(ch in s for ch in ".eEn"):
        s += ".0"
    return s


def _line_offsets(src: str) -> List[int]:
    offs = [0]
    for line in src.splitlines(keepends=True):
        offs.append(offs[-1] + len(line))
    return offs


def _span(src: str, node: ast.AST) -> Tuple[int, int]:
    offs = _line_offsets(src)
    # ast col offsets are UTF-8 byte offsets; mutable modules are ASCII-checked by the gate
    return offs[node.lineno - 1] + node.col_offset, offs[node.end_lineno - 1] + node.end_col_offset


def _numeric_value(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = _numeric_value(node.operand)
        return -v if isinstance(node.op, ast.USub) else v
    raise EditError(f"not a numeric literal: {ast.dump(node)[:80]}")


def find_const(tree: ast.Module, name: str) -> ast.Assign:
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id == name:
            return node
    raise EditError(f"module-level constant {name} not found")


def numeric_constants(src: str) -> Dict[str, float]:
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = _numeric_value(node.value)
            except EditError:
                pass
    return out


def find_func(tree: ast.Module, name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise EditError(f"function {name} not found")


def _splice(src: str, start: int, end: int, text: str) -> str:
    b = src.encode()
    return (b[:start] + text.encode() + b[end:]).decode()


def _check(src: str) -> str:
    ast.parse(src)
    compile(src, "<candidate>", "exec")
    return src


def const_set(src: str, name: str, value: float) -> Tuple[str, Dict[str, Any]]:
    tree = ast.parse(src)
    node = find_const(tree, name)
    old = _numeric_value(node.value)
    s, e = _span(src, node.value)
    new_src = _splice(src, s, e, fmt_number(value))
    return _check(new_src), {"old": old, "new": float(fmt_number(value))}


def const_scale(src: str, name: str, factor: float) -> Tuple[str, Dict[str, Any]]:
    old = _numeric_value(find_const(ast.parse(src), name).value)
    if old == 0.0:
        raise EditError(f"{name} is 0; scaling is a no-op")
    return const_set(src, name, old * factor)


def const_add(src: str, name: str, delta: float) -> Tuple[str, Dict[str, Any]]:
    old = _numeric_value(find_const(ast.parse(src), name).value)
    return const_set(src, name, old + delta)


def _callee_text(src: str, call: ast.Call) -> str:
    s, e = _span(src, call.func)
    return src.encode()[s:e].decode()


def swap_call(src: str, func: str, old: str, new: str) -> Tuple[str, Dict[str, Any]]:
    tree = ast.parse(src)
    fn = find_func(tree, func)
    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and _callee_text(src, n) == old]
    if not calls:
        raise EditError(f"no call to {old} in {func}")
    # splice from the end so earlier offsets stay valid
    new_src = src
    for call in sorted(calls, key=lambda c: (c.func.lineno, c.func.col_offset), reverse=True):
        s, e = _span(new_src, call.func)
        new_src = _splice(new_src, s, e, new)
    return _check(new_src), {"old": old, "new": new, "count": len(calls)}


def insert_term(src: str, func: str, arg: str, coef: float) -> Tuple[str, Dict[str, Any]]:
    tree = ast.parse(src)
    fn = find_func(tree, func)
    if arg not in [a.arg for a in fn.args.args]:
        raise EditError(f"{func} has no argument {arg}")
    const = f"TERM_{func.upper()}_{arg.upper()}"
    if const in numeric_constants(src):
        raise EditError(f"{const} already inserted (tune it with const edits instead)")
    rets = [n for n in ast.walk(fn) if isinstance(n, ast.Return) and n.value is not None]
    if len(rets) != 1:
        raise EditError(f"{func} must have exactly one return with a value (has {len(rets)})")
    s, e = _span(src, rets[0].value)
    expr = src.encode()[s:e].decode()
    new_src = _splice(src, s, e, f"({expr}) + {const} * {arg}")
    # new constant goes right after the last module-level numeric constant
    tree2 = ast.parse(new_src)
    last = None
    for node in tree2.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                _numeric_value(node.value)
                last = node
            except EditError:
                pass
    lines = new_src.splitlines(keepends=True)
    insert_at = last.end_lineno if last is not None else 0
    lines.insert(insert_at, f"{const} = {fmt_number(coef)}  # inserted by selfmod insert_term\n")
    return _check("".join(lines)), {"const": const, "coef": float(fmt_number(coef)), "expr": expr}


def reorder(src: str, func: str, index: int) -> Tuple[str, Dict[str, Any]]:
    tree = ast.parse(src)
    fn = find_func(tree, func)
    body = fn.body
    if isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]  # skip docstring
    if index < 0 or index + 1 >= len(body):
        raise EditError(f"{func}: cannot swap statements {index},{index + 1} of {len(body)}")
    a, b = body[index], body[index + 1]
    lines = src.splitlines(keepends=True)
    a_lines = lines[a.lineno - 1:a.end_lineno]
    b_lines = lines[b.lineno - 1:b.end_lineno]
    new_lines = lines[:a.lineno - 1] + b_lines + lines[a.end_lineno:b.lineno - 1] + a_lines + lines[b.end_lineno:]
    new_src = "".join(new_lines)
    if new_src == src:
        raise EditError("reorder produced identical source")
    return _check(new_src), {"swapped": [ast.unparse(a)[:60], ast.unparse(b)[:60]]}


def diff(old: str, new: str, path: str) -> str:
    return "".join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                         fromfile=f"a/{path}", tofile=f"b/{path}"))


TRANSFORMS = {
    "const_scale": lambda src, p: const_scale(src, p["target"], p["factor"]),
    "const_add": lambda src, p: const_add(src, p["target"], p["delta"]),
    "const_set": lambda src, p: const_set(src, p["target"], p["value"]),
    "swap_call": lambda src, p: swap_call(src, p["target"], p["old"], p["new"]),
    "insert_term": lambda src, p: insert_term(src, p["target"], p["arg"], p["coef"]),
    "reorder": lambda src, p: reorder(src, p["target"], p["index"]),
}


def apply(src: str, proposal: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    kind = proposal["kind"]
    if kind not in TRANSFORMS:
        raise EditError(f"unknown transform {kind}")
    return TRANSFORMS[kind](src, proposal)
