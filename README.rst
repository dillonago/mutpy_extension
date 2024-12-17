CS230 MutPy Instructions
=====

We will be going over how to setup, run, and test MutPy.

First clone this repository and install MutPy.

```$ git clone https://github.com/njhuey/mutpy.git```
```$ cd mutpy/```
```$ pip3 install .```

To run MutPy, we need a target file and a test file. The target file, which will come after the `--target` flag, contains the source code that will be mutated. The test file, which holds the test cases for the target file, will come after the `--unit-test` flags.

Here is the command for running MutPy: 
```$ mut.py --target target_file --unit-test test_file -m```

With the `-m` flag, we are able to see all of the mutations created and ran on the test file, as well as the result on if the mutant was killed, survived, was incompetent, or timed out. 
On the README file, many flags of features are listed to help customize parameters, some being the timeout factor, listing all the type of mutators, and choosing to run on certain mutators.\\
Running without the `--operator` flag means it will run all mutations available, meaning all of the default MutPy mutators as well as the ones we extended. If the user would like to test a subset of mutators, for example the NumPy mutators we implemented, the user can run MutPy on a target file and test file using the `--operator` flag and choose the specific operator to run. Here is the command to run just the NumPy function mutations: 

```$ mut.py --target target_file --unit-test test_file -m --operator NPM```

If there are multiple operators the user would like to run, MutPy allows them to stack operators. Here is an example command below: 

```$ mut.py --target target_file --unit-test test_file -m --operator NPM TCH```

To replicate our process of running MutPy on SciPy, an open source library built on top of NumPy with a wide range of functions for the scientific computing domain, the user first must build SciPy from source. The instructions can be found \href{https://docs.scipy.org/doc/scipy/building/index.html#building-from-source}{here}, or at this link (https://docs.scipy.org/doc/scipy/building/index.html#building-from-source). 
After following the instructions and the user is in the mamba/conda development environment, the user can run this command to verify the test cases in the test file are being ran correctly: 

```$ pytest scipy/linalg/tests/test_basic.py```

Once all the tests are passed, we can run MutPy on the source code and test file. In the environment, cd to the cloned MutPy directory and install the MutPy module. This is important to make sure the code changes and extensions added to MutPy are executed correctly. After this step is done, cd back into the cloned SciPy directory and the user is able to run MutPy on the files in the library. We focused on the \textunderscore basic.py file and the test\textunderscore basic.py test file in our evaluations, and here are some example commands to run MutPy on SciPy. 

```$ mut.py --target scipy/linalg/_basic.py --unit-test scipy/linalg/tests/test_basic.py -m```

```$ mut.py --target scipy/linalg/_basic.py --unit-test scipy/linalg/tests/test_basic.py -m --operator NPM```

```$ mut.py --target scipy/linalg/_basic.py --unit-test scipy/linalg/tests/test_basic.py -m --operator TCH```

Original MutPy Instructions
=====

|Python Versions| |Build Status| |Coverage Status| |Code Climate|

MutPy is a mutation testing tool for Python 3.3+ source code. MutPy
supports standard unittest module, generates YAML/HTML reports and has
colorful output. It applies mutation on AST level. You could boost your
mutation testing process with high order mutations (HOM) and code
coverage analysis.

Mutation testing
----------------

From article at Wikipedia:

    **Mutation testing** (or Mutation analysis or Program mutation)
    evaluates the quality of software tests. Mutation testing involves
    modifying a program's source code or byte code in small ways. A test
    suite that does not detect and reject the mutated code is considered
    defective. These so-called mutations, are based on well-defined
    mutation operators that either mimic typical programming errors
    (such as using the wrong operator or variable name) or force the
    creation of valuable tests (such as driving each expression to
    zero). The purpose is to help the tester develop effective tests or
    locate weaknesses in the test data used for the program or in
    sections of the code that are seldom or never accessed during
    execution.

Installation
------------

You can easily install MutPy from PyPi:

::

    $ pip install mutpy

... or if you want to have latest changes you can clone this repository
and install MutPy from sources:

::

    $ git clone git@github.com:mutpy/mutpy.git
    $ cd mutpy/
    $ python3 setup.py install

Example
-------

Main code (``calculator.py``) - we will mutate it:

.. code:: python

    def mul(x, y):
        return x * y

Test (``test_calculator.py``) - we will check its quality:

.. code:: python

    from unittest import TestCase
    from calculator import mul

    class CalculatorTest(TestCase):

        def test_mul(self):
            self.assertEqual(mul(2, 2), 4)

Now we can run MutPy in the same directory where we have our sources
files:

::

    $ mut.py --target calculator --unit-test test_calculator -m

This command will produce the following output:

::

    [*] Start mutation process:
       - targets: calculator
       - tests: test_calculator
    [*] All tests passed:
       - test_calculator [0.00031 s]
    [*] Start mutants generation and execution:
       - [#   1] AOR calculator.py:2  :
    --------------------------------------------------------------------------------
     1: def mul(x, y):
    ~2:     return x / y
    --------------------------------------------------------------------------------
    [0.02944 s] killed by test_mul (test_calculator.CalculatorTest)
       - [#   2] AOR calculator.py:2  :
    --------------------------------------------------------------------------------
     1: def mul(x, y):
    ~2:     return x // y
    --------------------------------------------------------------------------------
    [0.02073 s] killed by test_mul (test_calculator.CalculatorTest)
       - [#   3] AOR calculator.py:2  :
    --------------------------------------------------------------------------------
     1: def mul(x, y):
    ~2:     return x ** y
    --------------------------------------------------------------------------------
    [0.01152 s] survived
       - [#   4] SDL calculator.py:2  :
    --------------------------------------------------------------------------------
     1: def mul(x, y):
    ~2:     pass
    --------------------------------------------------------------------------------
    [0.01437 s] killed by test_mul (test_calculator.CalculatorTest)
    [*] Mutation score [0.21818 s]: 75.0%
       - all: 4
       - killed: 3 (75.0%)
       - survived: 1 (25.0%)
       - incompetent: 0 (0.0%)
       - timeout: 0 (0.0%)

First of all we run MutPy with few parameters. The most important are:

-  ``--target`` - after this flag we should pass module which we want to
   mutate.
-  ``--unit-test`` - this flag point to our unit tests module.

There are few phases in mutation process which we can see on printed by
MutPy output (marked by star ``[*]``):

-  main code and tests modules loading,
-  run tests with original (not mutated) code base,
-  code mutation (main mutation phase),
-  results summary.

There are 4 mutants generated in main mutation phase - 3 of them are
killed and only 1 mutant survived. We can see all stats at the end of
MutPy output. In this case MutPy didn't generate any incompetent (raised
``TypeError``) and timeout (generated infinite loop) mutants. Our
mutation score (killed to all mutants ratio) is 75%.

To increase mutation score (100% is our target) we need to improve our
tests. This is a mutant which survived:

.. code:: python

    def mul(x, y):
        return x ** y

This mutant survived because our test check if ``2 * 2 == 4``. Also
``2 ** 2 == 4``, so this data aren't good to specify multiplication
operation. We should change it, eg:

.. code:: python

    from unittest import TestCase
    from calculator import mul

    class CalculatorTest(TestCase):

        def test_mul(self):
            self.assertEqual(mul(2, 3), 6)

We can run MutPy again and now mutation score is equal 100%.

Command-line arguments
----------------------

List of all arguments with which you can run MutPy:

-  ``-t TARGET [TARGET ...]``, ``--target TARGET [TARGET ...]`` - target
   module or package to mutate,
-  ``-u UNIT_TEST [UNIT_TEST ...]``,
   ``--unit-test UNIT_TEST [UNIT_TEST ...]`` - test class, test method,
   module or package with unit tests,
-  ``--runner RUNNER`` - currently supported are: unittest (default), pytest (experimental)
-  ``-m``, ``--show-mutants`` - show mutants source code,
-  ``-r REPORT_FILE``, ``--report REPORT_FILE`` - generate YAML report,
-  ``--report-html DIR_NAME`` - generate HTML report,
-  ``-f TIMEOUT_FACTOR``. ``--timeout-factor TIMEOUT_FACTOR`` - max
   timeout factor (default 5),
-  ``-d``, ``--disable-stdout`` - try disable stdout during mutation
   (this option can damage your tests if you interact with
   ``sys.stdout``),
-  ``-e``. ``--experimental-operators`` - use experimental operators,
-  ``-o OPERATOR [OPERATOR ...]``,
   ``--operator OPERATOR [OPERATOR ...]`` - use only selected operators,
-  ``--disable-operator OPERATOR [OPERATOR ...]`` - disable selected
   operators,
-  ``-l``. ``--list-operators`` - list available operators,
-  ``-p DIR``. ``--path DIR`` - extend Python path,
-  ``--percentage PERCENTAGE`` - percentage of the generated mutants
   (mutation sampling),
-  ``--coverage`` - mutate only covered code,
-  ``-h``, ``--help`` - show this help message and exit,
-  ``-v``, ``--version`` - show program's version number and exit,
-  ``-q``, ``--quiet`` - quiet mode,
-  ``--debug`` - debug mode,
-  ``-c``. ``--colored-output`` - try print colored output,
-  ``--order ORDER`` - mutation order,
-  ``--hom-strategy HOM_STRATEGY`` - HOM strategy,
-  ``--list-hom-strategies`` - list available HOM strategies,
-  ``--mutation-number MUTATION_NUMBER`` - run only one mutation (debug
   purpose).

Mutation operators
------------------

List of MutPy mutation operators sorted by alphabetical order:

-  AOD - arithmetic operator deletion
-  AOR - arithmetic operator replacement
-  ASR - assignment operator replacement
-  BCR - break continue replacement
-  COD - conditional operator deletion
-  COI - conditional operator insertion
-  CRP - constant replacement
-  DDL - decorator deletion
-  EHD - exception handler deletion
-  EXS - exception swallowing
-  IHD - hiding variable deletion
-  IOD - overriding method deletion
-  IOP - overridden method calling position change
-  LCR - logical connector replacement
-  LOD - logical operator deletion
-  LOR - logical operator replacement
-  ROR - relational operator replacement
-  SCD - super calling deletion
-  SCI - super calling insert
-  SIR - slice index remove

Experimental mutation operators:

-  CDI - classmethod decorator insertion
-  OIL - one iteration loop
-  RIL - reverse iteration loop
-  SDI - staticmethod decorator insertion
-  SDL - statement deletion
-  SVD - self variable deletion
-  ZIL - zero iteration loop

Supported Test Runners
----------------------

Currently the following test runners are supported by MutPy:

- `unittest <https://docs.python.org/3/library/unittest.html>`_
- `pytest <https://docs.pytest.org/en/latest/>`_

License
-------

Licensed under the Apache License, Version 2.0. See LICENSE file.

MutPy was developed as part of engineer's and master’s thesis at
Institute of Computer Science, Faculty of Electronics and Information
Technology, Warsaw University of Technology.

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/MutPy.svg
   :target: https://github.com/mutpy/mutpy
.. |Build Status| image:: https://travis-ci.org/mutpy/mutpy.svg?branch=master
   :target: https://travis-ci.org/mutpy/mutpy
.. |Coverage Status| image:: https://coveralls.io/repos/github/mutpy/mutpy/badge.svg?branch=master
   :target: https://coveralls.io/github/mutpy/mutpy?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/mutpy/mutpy/badges/gpa.svg
   :target: https://codeclimate.com/github/mutpy/mutpy
