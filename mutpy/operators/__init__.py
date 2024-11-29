from .arithmetic import *
from .base import *
from .decorator import *
from .exception import *
from .inheritance import *
from .logical import *
from .loop import *
from .misc import *
from .numpy import *

SuperCallingInsert = utils.get_by_python_version(
    [
        SuperCallingInsertPython27,
        SuperCallingInsertPython35,
    ]
)

standard_operators = {
    ArgumentValueChanger,
    FloatTypeChanger,
    ComplexTypeChanger,
    ArithmeticOperatorDeletion,
    ArithmeticOperatorReplacement,
    AssignmentOperatorReplacement,
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
    any2all,
    all2any,
    zeros2ones,
    ones2zeros,
    average2mean,
    zeros2zeros_like,
    zeros_like2zeros,
    ones2ones_like,
    ones_like2ones
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
