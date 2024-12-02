from .arithmetic import *
from .base import *
from .decorator import *
from .exception import *
from .inheritance import *
from .logical import *
from .loop import *
from .misc import *
from .numpy import *

SuperCallingInsert = utils.get_by_python_version([
    SuperCallingInsertPython27,
    SuperCallingInsertPython35,
])

standard_operators = {
    ArgumentValueChanger,
    ArithmeticOperatorDeletion,
    ArithmeticOperatorReplacement,
    AssignmentOperatorReplacement,
    BreakContinueReplacement,
    ConditionalOperatorDeletion,
    ConditionalOperatorInsertion,
    ConstantReplacement,
    DecoratorDeletion,
    ExceptionHandlerDeletion,
    ExceptionSwallowing,
    HidingVariableDeletion,
    LogicalConnectorReplacement,
    LogicalOperatorDeletion,
    LogicalOperatorReplacement,
    OverriddenMethodCallingPositionChange,
    OverridingMethodDeletion,
    RelationalOperatorReplacement,
    SliceIndexRemove,
    SuperCallingDeletion,
    SuperCallingInsert,
    AnyMutator
}

experimental_operators = {
    ClassmethodDecoratorInsertion,
    OneIterationLoop,
    ReverseIterationLoop,
    SelfVariableDeletion,
    StatementDeletion,
    StaticmethodDecoratorInsertion,
    ZeroIterationLoop,
}
