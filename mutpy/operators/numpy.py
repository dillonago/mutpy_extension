import ast

from mutpy import utils
from mutpy.operators.arithmetic import AbstractArithmeticOperatorReplacement
from mutpy.operators.base import MutationOperator, MutationResign


class any2all(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "any":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="all", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class all2any(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "all":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="any", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class zeros2ones(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "zeros":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="ones", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class ones2zeros(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "ones":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="zeros", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class average2mean(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "average":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="mean", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class zeros2zeros_like(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "zeros":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="zeros_like", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class zeros_like2zeros(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "zeros_like":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="zeros", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()


class ones2ones_like(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "ones":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="ones_like", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()

class ones_like2ones(MutationOperator):
    def mutate_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "ones_like":
            name = node.func.value
            all_node = ast.Attribute(value=name, attr="ones", ctx=ast.Load())
            node.func = all_node
            return node
        raise MutationResign()