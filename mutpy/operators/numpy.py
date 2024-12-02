import ast

from mutpy import utils
from mutpy.operators.arithmetic import AbstractArithmeticOperatorReplacement
from mutpy.operators.base import MutationOperator, MutationResign


class AnyMutator(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "any":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="all", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()