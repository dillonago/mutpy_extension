from .arithmetic import *
from .base import *
from .decorator import *
from .exception import *
from .inheritance import *
from .logical import *
from .loop import *
from .misc import *

SuperCallingInsert = utils.get_by_python_version(
    [
        SuperCallingInsertPython27,
        SuperCallingInsertPython35,
    ]
)

standard_operators = {
    NumPyFunction,
    ArgumentValueChanger,
    FloatTypeChanger,
    ComplexTypeChanger,
    ArgumentAxis,
    ArgumentKeepDims,
    ResetIndexChanger,
    ArithmeticOperatorDeletion,
    ArithmeticOperatorReplacement,
    AssignmentOperatorReplacement,
    PandasMutator,
    NumpyMutator,
    TypeChanger,
    BreakContinueReplacement,
    ConditionalOperatorDeletion,
    ConditionalOperatorInsertion,
    ConstantReplacement,
    DecoratorDeletion,
    DefaultParameterMutation,
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
