import ast

from mutpy import utils
from mutpy.operators.arithmetic import AbstractArithmeticOperatorReplacement
from mutpy.operators.base import MutationOperator, MutationResign


class AssignmentOperatorReplacement(AbstractArithmeticOperatorReplacement):
    def should_mutate(self, node):
        return isinstance(node.parent, ast.AugAssign)

    @classmethod
    def name(cls):
        return 'ASR'


class BreakContinueReplacement(MutationOperator):
    def mutate_Break(self, node):
        return ast.Continue()

    def mutate_Continue(self, node):
        return ast.Break()


class ConstantReplacement(MutationOperator):
    FIRST_CONST_STRING = 'mutpy'
    SECOND_CONST_STRING = 'python'

    def mutate_Constant(self, node):
        if isinstance(node.value, (int, float)):  # Handle numbers
            return ast.Constant(value=node.value + 1)

        elif isinstance(node.value, str):  # Handle strings
            if utils.is_docstring(node):
                raise MutationResign()

            if node.value != self.FIRST_CONST_STRING:
                return ast.Constant(value=self.FIRST_CONST_STRING)
            else:
                return ast.Constant(value=self.SECOND_CONST_STRING)

        elif node.value is not None:  # Handle NameConstant (True, False, None)
            return ast.Constant(value=None)

        raise MutationResign()  # Skip mutation if the constant isn't relevant

    def mutate_Constant_empty(self, node):
        if isinstance(node.value, str) and node.value and not utils.is_docstring(node):
            return ast.Constant(value='')  # Replace non-empty strings with empty strings

        raise MutationResign()  # Skip for non-string nodes or docstrings

    @classmethod
    def name(cls):
        return 'CRP'

class SliceIndexRemove(MutationOperator):
    def mutate_Slice_remove_lower(self, node):
        if not node.lower:
            raise MutationResign()

        return ast.Slice(lower=None, upper=node.upper, step=node.step)

    def mutate_Slice_remove_upper(self, node):
        if not node.upper:
            raise MutationResign()

        return ast.Slice(lower=node.lower, upper=None, step=node.step)

    def mutate_Slice_remove_step(self, node):
        if not node.step:
            raise MutationResign()

        return ast.Slice(lower=node.lower, upper=node.upper, step=None)


class SelfVariableDeletion(MutationOperator):
    def mutate_Attribute(self, node):
        try:
            if node.value.id == 'self':
                return ast.Name(id=node.attr, ctx=ast.Load())
            else:
                raise MutationResign()
        except AttributeError:
            raise MutationResign()


class StatementDeletion(MutationOperator):
    def mutate_Assign(self, node):
        return ast.Pass()

    def mutate_Return(self, node):
        return ast.Pass()

    def mutate_Expr(self, node):
        if utils.is_docstring(node.value):
            raise MutationResign()
        return ast.Pass()

    @classmethod
    def name(cls):
        return 'SDL'
