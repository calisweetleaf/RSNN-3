"""Dependency-free structural checks for the theorem-driven substrate."""

import ast
import unittest
from pathlib import Path


SOURCE = Path(__file__).with_name("autodidactic_learning.py")
THEOREMS = Path(__file__).with_name("theorems")


class SubstrateStaticTests(unittest.TestCase):
    def test_source_compiles(self):
        ast.parse(SOURCE.read_text(encoding="utf-8"))


    def test_train_contract_is_present(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        self.assertTrue({"run_training_cycle", "_bayesian_update", "_acquire_knowledge"} <= names)


    def test_core_documents_are_present(self):
        expected = {
            "Recursive_Abstract_Laddering.md",
            "Recursive Learning Architechture.md",
            "RAL_Framework.md",
            "RAL_Bridge.md",
            "Bayesian_Updating_System.md",
            "enhanced-rlm.md",
            "enhanced_URSMIFv1.md",
        }
        self.assertGreaterEqual({path.name for path in THEOREMS.iterdir()}, expected)


if __name__ == "__main__":
    unittest.main()
