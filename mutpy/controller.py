import random
import sys
import time

import groq
import os
import ast
import pprint
import inspect

from difflib import unified_diff
from mutpy import views, utils, codegen, termcolor

import unittest

class TestsFailAtOriginal(Exception):

    def __init__(self, result=None):
        self.result = result


class MutationScore:

    def __init__(self):
        self.killed_mutants = 0
        self.timeout_mutants = 0
        self.incompetent_mutants = 0
        self.survived_mutants = 0
        self.covered_nodes = 0
        self.all_nodes = 0

    def count(self):
        bottom = self.all_mutants - self.incompetent_mutants
        return (
            (((self.killed_mutants + self.timeout_mutants) / bottom) * 100)
            if bottom
            else 0
        )

    def inc_killed(self):
        self.killed_mutants += 1

    def inc_timeout(self):
        self.timeout_mutants += 1

    def inc_incompetent(self):
        self.incompetent_mutants += 1

    def inc_survived(self):
        self.survived_mutants += 1

    def update_coverage(self, covered_nodes, all_nodes):
        self.covered_nodes += covered_nodes
        self.all_nodes += all_nodes

    @property
    def all_mutants(self):
        return (
            self.killed_mutants
            + self.timeout_mutants
            + self.incompetent_mutants
            + self.survived_mutants
        )


class MutationController(views.ViewNotifier):

    def __init__(
        self,
        runner_cls,
        target_loader,
        test_loader,
        views,
        mutant_generator,
        timeout_factor=5,
        disable_stdout=False,
        mutate_covered=False,
        mutation_number=None,
    ):
        super().__init__(views)
        self.target_loader = target_loader
        self.test_loader = test_loader
        self.mutant_generator = mutant_generator
        self.timeout_factor = timeout_factor
        self.stdout_manager = utils.StdoutManager(disable_stdout)
        self.mutation_number = mutation_number
        self.test_new_loader = utils.ModulesLoader(['llmtestsuite'], None)
        self.client = groq.Client(api_key="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")
        self.history = []
        self.counter = 0
        self.runner = runner_cls(
            self.test_loader, self.timeout_factor, self.stdout_manager, mutate_covered
        )

    def run(self):
        self.notify_initialize(self.target_loader.names, self.test_loader.names)
        try:
            timer = utils.Timer()
            self.run_mutation_process()
            self.notify_end(self.score, timer.stop())
        except TestsFailAtOriginal as error:
            self.notify_original_tests_fail(error.result)
            sys.exit(-1)
        except utils.ModulesLoaderException as error:
            self.notify_cant_load(error.name, error.exception)
            sys.exit(-2)

    def run_mutation_process(self):
        try:
            test_modules, total_duration, number_of_tests = self.load_and_check_tests()

            self.notify_passed(test_modules, number_of_tests)
            #Start Gradio here


            self.notify_start()

            self.score = MutationScore()

            for target_module, to_mutate in self.target_loader.load(
                [module for module, *_ in test_modules]
            ):
                # Pass in test_modules[0][0] to get the original test suite. 
                self.mutate_module(target_module, to_mutate, total_duration, test_modules[0][0])
        except KeyboardInterrupt:
            pass

    # Check if tests pass initially. 
    def new_load_and_test(self, file_name):
        test_modules = []
        number_of_tests = 0
        total_duration = 0
        passedInitially = True
        errorMessage = None
        # print(file_name)
        for test_module, target_test in utils.ModulesLoader([file_name], None).load():
            # print(test_module)
            # print(inspect.getsource(test_module))
            try: 
                result, duration = self.run_test(test_module, target_test)
                # print(result.failed[0].name)
                if not result.was_successful():
                    raise TestsFailAtOriginal(result)
                test_modules.append((test_module, target_test, duration))

            except TestsFailAtOriginal as e:
                # If test case doesn't pass initially.
                print('\nError Message: ')
                print(e.result.get_exception_traceback())
                passedInitially = False
                errorMessage = e.result.get_exception_traceback()

                # self.reprompt(e.result.get_exception_traceback())

                # reprompt_count=3
                # for x in range(1, reprompt_count):
                #     self.reprompt()

        number_of_tests += result.tests_run()
        total_duration += duration

        return test_modules, total_duration, number_of_tests, passedInitially, errorMessage

    def load_and_check_tests(self):
        test_modules = []
        number_of_tests = 0
        total_duration = 0
        for test_module, target_test in self.test_loader.load():
            result, duration = self.run_test(test_module, target_test)
            if result.was_successful():
                test_modules.append((test_module, target_test, duration))
            else:
                raise TestsFailAtOriginal(result)
            number_of_tests += result.tests_run()
            total_duration += duration

        return test_modules, total_duration, number_of_tests

    def run_test(self, test_module, target_test):
        return self.runner.run_test(test_module, target_test)
    
    def reprompt(self, error, diff_code):
        print("Reprompting...")
        if(type(error)==type(None)):
            error="None"
        # print(self.history)\
        question = [{"role": "user", "content": "The last test case you gave did not pass without the mutation.\
        The error that made it not pass is this: " + error + "\n\
        Use the error to revise the test case. Rewrite the test case to pass without the mutant and fail when ran with the mutant. The mutant is this:\
        " + diff_code + "\nThe only thing in the response should be the revised test case and nothing else. It should follow Python unit test syntax.\
        Do not start with anything else but def..."}]
        # question = [{"role": "user", "content": "The last test case you gave did not pass initially.\
        # Rewrite the test case to pass without the mutant and fail when ran with the mutant. The mutant is this:\
        # " + diff_code + "\nThe only thing in the response should be the revised test case and nothing else. It should follow Python unit test syntax.\
        # Do not start with anything else but def..."}]
        self.history = [self.history[len(self.history)-1]] + question
        # print(chat_history_new)


        # response = self.client.chat.completions.create(model="llama3-70b-8192",
        #                                         messages=self.history,
        #                                         max_tokens=1000,
        #                                         temperature=1.2)
        response = self.client.chat.completions.create(model="llama-3.3-70b-versatile",
                                                messages=self.history,
                                                max_tokens=1000,
                                                temperature=1.2)
        # response = self.client.chat.completions.create(model="deepseek-r1-distill-llama-70b",
        #                                         messages=self.history,
        #                                         max_tokens=1000,
        #                                         temperature=1.2)
        self.history.append({
                "role": "assistant",
                "content": response.choices[0].message.content
        })

        print(response.choices[0].message.content)
        return response.choices[0].message.content

    def reprompt_passed(self, diff_code):
        print("Passed initially, reprompting...")
        question = [{"role": "user", "content": "The last test case passed initially but did not kill the mutant.\
        Rewrite the test case to pass without the mutant and fail when ran with the mutant. The mutant is this: \n\
        " + diff_code + "\nThe only thing in the response should be the revised test case and nothing else. It should follow Python unit test syntax.\
        Do not start with anything else but def..."}]
        self.history = [self.history[len(self.history)-1]] + question
        # print(self.history[0]["content"])
        # print(self.history[1]["content"])
        # response = self.client.chat.completions.create(model="llama3-70b-8192",
        #                                         messages=self.history,
        #                                         max_tokens=1000,
        #                                         temperature=1.2)
        response = self.client.chat.completions.create(model="llama-3.3-70b-versatile",
                                                messages=self.history,
                                                max_tokens=1000,
                                                temperature=1.2)
        # response = self.client.chat.completions.create(model="deepseek-r1-distill-llama-70b",
        #                                         messages=self.history,
        #                                         max_tokens=1000,
        #                                         temperature=1.2)
        self.history.append({
                "role": "assistant",
                "content": response.choices[0].message.content
        })
        print(response.choices[0].message.content)
        return response.choices[0].message.content



    def create_suite(self, test_suite, function_def):
        # print("Testing output:")
        # print(function_def)
        # Add test case to module: 
        # print(inspect.getsource(test_suite))
        # print(type(test_suite)
        test_ast = self.create_target_ast(test_suite)
        # print(test_ast)
        # print(test_ast)
        # for x in test_ast.body:
        #     if(isinstance(x, ast.ClassDef)):
        #         print(ast.unparse(x))
        # print(ast.dump(test_ast, indent=4)) 


        # Replace this with the output of the LLM
        # function_deftest = "def test comMul2(self):\n \
        #     data = np.random.rand(2,3).astype(np.complex128)\n \
        #     df = pd.DataFrame(data)\n \
        #     num = np.complex64(np.random.rand())\n \
        #     df_mul = df*num\n \
        #     output = df_mul.equals(comMul(df, num))\n \
        #     self.assertFalse(output)"

        # print(function_def)

        try:
            module_node = ast.parse(function_def)
            # module_node = ast.parse(function_deftest)
        except SyntaxError as e: 
            error_syntax = f"Syntax error: {e}"
            return error_syntax
        else: 
            module_node = ast.parse(function_def)
            func_node = module_node.body[0]
            for node in test_ast.body:
                if isinstance(node, ast.ClassDef): 
                    node.body.append(func_node)
                    break
            # print(ast.dump(func_node, indent=4))
            # print(test_ast.body[0])
            uptest = ast.unparse(test_ast)

            file_name = "llmtestsuite" + str(self.counter) + ".py"
            # print(file_name)
            self.counter+=1
            with open(file_name, "w") as f:
                f.write(uptest)
            # Check if new test passes initially
            # print(uptest)
            # print(test_modules)
            # print(number_of_tests)
            return file_name
            # print(mutant_ast)
            # print(mutant_module)

    def prompt_llm(self, diff_code, test_suite):

        '''
        Prompt Strategies: 
        Clear instructions
        Provide reference text
        Split complex tasks into simple subtasks
        '''
        test_ast = self.create_target_ast(test_suite)
        # print(test_ast)
        # print(test_ast)
        updated_suite = ""
        for x in test_ast.body:
            if(isinstance(x, ast.ClassDef)):
                updated_suite = ast.unparse(x)
        
        # few_shot = [
        #     {"role": "system", "content": "Only respond with a single test case. Do not respond with the reasoning unless asked. I will give some examples of sample mutations with valid responses as well as the test suite where the mutation survives.\
        #     The goal is to kill the mutated code while making sure the generated test case still passes with the initial source code.\
        #     This means that the test case passes initially and fails when a mutation is applied to the code.\
        #     I will also give some examples of responses that satisfy these conditions.\
        #     The test case should not only pass initially without the mutation, but kill the mutation as well. Only respond with the test case itself with no explanations or extra.\
        #     The response should start with def ... and the test case should follow the syntax for a Python unit test test case. Make sure the test case name is acceptable."},

        #     {"role": "user", "content": "Example 1:\n\
        #     Given this mutation:\n\
        #     4: def div(x, y):\n\
        #     - 5:     return x / y\n\
        #     + 5:     return x // y\n\
        #     and the existing test suite where the mutation survives:\n\
        #     def test_div(self):\n\t\
        #     self.assertEqual(div(3, 2), 1.5)\n\
        #     Output a test case that will kill the mutation while passing without the mutation."},

        #     {"role": "assistant", "content": "def test_div2(self):\n\t\
        #     self.assertEqual(div(3, 2), 1.5)"},

        #     {"role": "user", "content": "Example 2: Given this mutation:\n\
        #     1: def mul(x, y):\n\
        #     -  2:     return x * y\n\
        #     +  2:     return x ** y\n\
        #     and the existing test suite where the mutation survives:\n\
        #     def test_mul(self):\n\t\
        #     self.assertEqual(mul(2, 2), 4)\n\
        #     Output a test case that will kill the mutation while passing without the mutation."},
        #     {"role": "assistant", "content": "def test_mul2(self):\n\t\
        #     self.assertEqual(mul(3, 2), 9)"}
        # ]
        # question = [{"role": "user", "content": "User: Given this mutation:\n" + diff_code + "\n\
        #     and the existing test suite where the mutation survives:\n" + updated_suite + "\n\
        #     Output a test case that will kill the mutation while passing without the mutation. The only thing in the response should be the test case and nothing else. It should follow Python unit test syntax.\
        #     Do not start with anything else but def..."}]
        
        few_shot = [
            {"role": "system", "content": "Only respond with a single test case. Do not respond with the thinking unless asked.\
            The goal is to catch and kill the mutation while making sure the generated test case still passes initially.\
            This means that the test case passes initially and fails when a mutation is applied to the code.\
            The test case should not only pass initially without the mutation, but kill the mutation as well. Only respond with the test case itself with no explanations or extra.\
            The response should start with def ... and the test case should follow the syntax for a Python unit test test case."} 
            # {"role": "system", "content": "Only respond with a single test case. Do not respond with the thinking unless asked. I will give some few shot examples of sample mutations as well as sample test cases.\
            # The test cases are meant for syntax purposes and is a Python unit test test case.\
            # I will also give some valid responses.\
            # The goal is to catch and kill the mutation while making sure the generated test case still passes initially.\
            # This means that the test case passes initially and fails when a mutation is applied to the code.\
            # The test case should not only pass initially without the mutation, but kill the mutation as well. Only respond with the test case itself with no explanations or extra.\
            # The response should start with def ... and the test case should follow the syntax for a Python unit test test case."},
            # {"role": "user", "content": "Example 1:\n\
            # Given this mutation:\n\
            # 4: def div(x, y):\n\
            # - 5:     return x / y\n\
            # + 5:     return x // y\n\
            # and the existing test suite where the mutation survives:\n\
            # def test_div(self):\n\t\
            # self.assertEqual(div(3, 2), 1.5)\n\
            # Output a test case that will kill the mutation while passing without the mutation."},

            # {"role": "assistant", "content": "def test_div2(self):\n\t\
            # self.assertEqual(div(3, 2), 1.5)"},

            # {"role": "user", "content": "Example 2: Given this mutation:\n\
            # 1: def mul(x, y):\n\
            # -  2:     return x * y\n\
            # +  2:     return x ** y\n\
            # and the existing test suite where the mutation survives:\n\
            # def test_mul(self):\n\t\
            # self.assertEqual(mul(2, 2), 4)\n\
            # Output a test case that will kill the mutation while passing without the mutation."},
            # {"role": "assistant", "content": "def test_mul2(self):\n\t\
            # self.assertEqual(mul(3, 2), 9)"}
        ]
        test1 = "def test_empty(self, dt_ab, dt_b):\n\t\
                ab = np.array([[]], dtype=dt_ab)\n\
                b = np.array([], dtype=dt_b)\n\
                x = solveh_banded(ab, b)\n\
                self.assertEqual(x.shape, (0,))\n\
                self.assertEqual(x.dtype, solve(np.eye(1, dtype=dt_ab), np.ones(1, dtype=dt_b)).dtype)\n\
                b = np.empty((0, 0), dtype=dt_b)\n\
                x = solveh_banded(ab, b)\n\
                self.assertEqual(x.shape, (0, 0))\n\
                self.assertEqual(x.dtype, solve(np.eye(1, dtype=dt_ab), np.ones(1, dtype=dt_b)).dtype)"

        test2 = "def test_simple_pos_complexb(self):\n\t\
                a = [[5, 2], [2, 4]]\n\
                for b in ([1j, 0],\n\
                        [[1j, 1j], [0, 2]],\n\
                        ):\n\
                    x = solve(a, b, assume_a='pos')\n\
                    assert_array_almost_equal(dot(a, x), b)"
        
        question = [{"role": "user", "content": "User: Given this mutation:\n" + diff_code + "\n\
            and some example tests include\nExample 1:\n" + test1 + "\n Example 2:\n" + test2 + "\n\
            Output a test case that will kill the mutation while passing without the mutation. The only thing in the response should be the test case and nothing else. It should follow Python unit test syntax.\
            Do not start with anything else but def..."}]


        self.history = few_shot + question
        # print(question[0]["content"])

        # response = self.client.chat.completions.create(model="llama3-70b-8192",
        #                                         messages=self.history,
        #                                         max_tokens=1000,
        #                                         temperature=1.2)
        response = self.client.chat.completions.create(model="llama-3.3-70b-versatile",
                                                messages=self.history,
                                                max_tokens=1000,
                                                temperature=1.2)
        # response = self.client.chat.completions.create(model="deepseek-r1-distill-llama-70b",
        #                                         messages=self.history,
        #                                         max_tokens=1000,
        #                                         temperature=1.2)
        self.history.append({
                "role": "assistant",
                "content": response.choices[0].message.content
        })
        print(response.choices[0].message.content)
        return response.choices[0].message.content

        # print(result.exception)
        # print(result.exception_traceback)
        # print(result.killer)



    @utils.TimeRegister
    def mutate_module(self, target_module, to_mutate, total_duration, test_suite):
        # Prints that were here: 
        # print(inspect.getsource(target_module))
        # pprint.pprint(ast.dump(target_ast, indent=4))
        # print(mutations[0])
        # pprint.pprint(ast.dump(mutant_ast))
        target_ast = self.create_target_ast(target_module)
        coverage_injector, coverage_result = self.inject_coverage(target_ast, target_module)
        if coverage_injector:
            self.score.update_coverage(*coverage_injector.get_result())
        for mutations, mutant_ast in self.mutant_generator.mutate(target_ast, to_mutate, coverage_injector,
                                                                  module=target_module):
            diff_code = self.get_diff_code(mutant_ast, ast.parse(inspect.getsource(target_module)))
            mutation_number = self.score.all_mutants + 1
            if self.mutation_number and self.mutation_number != mutation_number:
                self.score.inc_incompetent()
                continue
            self.notify_mutation(mutation_number, mutations, target_module, mutant_ast)
            mutant_module = self.create_mutant_module(target_module, mutant_ast)
            if mutant_module:
                self.run_tests_with_mutant(total_duration, mutant_module, mutations, coverage_result, test_suite, diff_code)
            else:
                self.score.inc_incompetent()

    def get_diff_code(self, mutant, original):
        mutant_src = codegen.to_source(mutant)
        mutant_src = codegen.add_line_numbers(mutant_src)
        original_src = codegen.to_source(original)
        original_src = codegen.add_line_numbers(original_src)
        diff_code = self._print_diff(mutant_src, original_src)
        # print(diff_code)
        return diff_code

    def _print_diff(self, mutant_src, original_src):
        diff = self._create_diff(mutant_src, original_src)
        diff = [line for line in diff if not line.startswith(('---', '+++', '@@'))]
        diff = [self.decorate(line, 'blue') if line.startswith('- ') else line for line in diff]
        diff = [self.decorate(line, 'green') if line.startswith('+ ') else line for line in diff]
        diff_thing = "\n".join(diff)
        return diff_thing
        # print("\n{}\n".format('-' * 80) + "\n".join(diff) + "\n{}".format('-' * 80))

    @staticmethod
    def _create_diff(mutant_src, original_src):
        return list(unified_diff(original_src.split('\n'), mutant_src.split('\n'), n=4, lineterm=''))

    def decorate(self, text, color=None, on_color=None, attrs=None, colored_output=False):
        if colored_output:
            return termcolor.colored(text, color, on_color, attrs)
        else:
            return text


    def inject_coverage(self, target_ast, target_module):
        return self.runner.inject_coverage(target_ast, target_module)

    @utils.TimeRegister
    def create_target_ast(self, target_module):
        with open(target_module.__file__) as target_file:
            return utils.create_ast(target_file.read())

    @utils.TimeRegister
    def create_mutant_module(self, target_module, mutant_ast):
        try:
            with self.stdout_manager:
                return utils.create_module(
                    ast_node=mutant_ast, module_name=target_module.__name__
                )
        except BaseException as exception:
            self.notify_incompetent(0, exception, tests_run=0)
            return None


    @utils.TimeRegister
    def run_test_again_with_mutant(self, total_duration, mutant_module, mutations, coverage_result, test_suite, suite):
        # print(suite.suite)
        # print(test_suite)
        if coverage_result:
            self.mark_not_covered_tests_as_skip(mutations, coverage_result, suite)
        timer = utils.Timer()
        result = self.runner.run_mutation_test_runner(suite, total_duration)
        timer.stop()
        return result, timer.duration


    def run_tests_with_mutant(
        self, total_duration, mutant_module, mutations, coverage_result, test_suite, diff_code
    ):
        result, duration = self.runner.run_tests_with_mutant(
            total_duration, mutant_module, mutations, coverage_result
        )

        #Prompt LLM, get test case, run it initially. 
        #count: number of times to reprompt when failing initially
        # UNCOMMENT HERE
        if(result!=None and result.is_survived==True):
            count = 0
            function_def = self.prompt_llm(diff_code, test_suite)
            fileName = self.create_suite(test_suite, function_def)
            #test the output
            if fileName[0]=='S':
                passedInitially = False
                errorMessage = fileName
            else: 
                test_modules, total_duration, number_of_tests, passedInitially, errorMessage = self.new_load_and_test(fileName)
            print("Passed initially: " + str(passedInitially))
            # print(number_of_tests)
            while(passedInitially==False and count<2):
                print("Count: " + str(count))
                function_def_updated = self.reprompt(errorMessage, diff_code)
                fileName = self.create_suite(test_suite, function_def_updated)
                if fileName[0]=='S':
                    errorMessage=fileName
                    passedInitially=False
                else: 
                    test_modules, total_duration, number_of_tests, passedInitially, errorMessage = self.new_load_and_test(fileName)
                count+=1
            if(passedInitially==True):
                suite = self.runner.create_llm_test_suite(mutant_module, fileName)
                # print(suite.suite)
                result, total_duration = self.run_test_again_with_mutant(total_duration, mutant_module, mutations, coverage_result, test_suite, suite)
                # print(result.tests_run)
                if(result.killer=="None"):
                    func_def = self.reprompt_passed(diff_code)
                    fileName = self.create_suite(test_suite, func_def)
                    if fileName[0]=='S':
                        errorMessage=fileName
                        passedInitially=False
                    else: 
                        test_modules, total_duration, number_of_tests, passedInitially, errorMessage = self.new_load_and_test(fileName)
                    if(passedInitially==False):
                        print("Did not pass initially after change.")
                        if fileName[0]!='S':
                            suite = self.runner.create_llm_test_suite(mutant_module, fileName)
                            # print(suite.suite)
                            result, total_duration = self.run_test_again_with_mutant(total_duration, mutant_module, mutations, coverage_result, test_suite, suite)
                            if(type(result)!=type(None)):
                                print("Partially correct:" + result.killer)
                                result.is_survived=True
                        else:
                            print("SYNTAX ERROR HERE")
                    else:
                        print("Passed intitially, checking")
                        suite = self.runner.create_llm_test_suite(mutant_module, fileName)
                        # print(suite.suite)
                        result, total_duration = self.run_test_again_with_mutant(total_duration, mutant_module, mutations, coverage_result, test_suite, suite)
                        if(result.is_survived==True):
                            print("Survived")
                        else:
                            print("killed with "+ result.killer)
            else: 
                print("Skipped, did not pass even with reprompt.")

        self.update_score_and_notify_views(result, duration)

    def update_score_and_notify_views(self, result, mutant_duration):
        if not result:
            self.update_timeout_mutant(mutant_duration)
        elif result.is_incompetent:
            self.update_incompetent_mutant(result, mutant_duration)
        elif result.is_survived:
            self.update_survived_mutant(result, mutant_duration)
        else:
            self.update_killed_mutant(result, mutant_duration)

    def update_timeout_mutant(self, duration):
        self.notify_timeout(duration)
        self.score.inc_timeout()

    def update_incompetent_mutant(self, result, duration):
        self.notify_incompetent(duration, result.exception, result.tests_run)
        self.score.inc_incompetent()

    def update_survived_mutant(self, result, duration):
        self.notify_survived(duration, result.tests_run)
        self.score.inc_survived()

    def update_killed_mutant(self, result, duration):
        self.notify_killed(
            duration, result.killer, result.exception_traceback, result.tests_run
        )
        self.score.inc_killed()


class HOMStrategy:

    def __init__(self, order=2):
        self.order = order

    def remove_bad_mutations(
        self, mutations_to_apply, available_mutations, allow_same_operators=True
    ):
        for mutation_to_apply in mutations_to_apply:
            for available_mutation in available_mutations[:]:
                if (
                    mutation_to_apply.node == available_mutation.node
                    or mutation_to_apply.node in available_mutation.node.children
                    or available_mutation.node in mutation_to_apply.node.children
                    or (
                        not allow_same_operators
                        and mutation_to_apply.operator == available_mutation.operator
                    )
                ):
                    available_mutations.remove(available_mutation)


class FirstToLastHOMStrategy(HOMStrategy):
    name = "FIRST_TO_LAST"

    def generate(self, mutations):
        mutations = mutations[:]
        while mutations:
            mutations_to_apply = []
            index = 0
            available_mutations = mutations[:]
            while len(mutations_to_apply) < self.order and available_mutations:
                try:
                    mutation = available_mutations.pop(index)
                    mutations_to_apply.append(mutation)
                    mutations.remove(mutation)
                    index = 0 if index == -1 else -1
                except IndexError:
                    break
                self.remove_bad_mutations(mutations_to_apply, available_mutations)
            yield mutations_to_apply


class EachChoiceHOMStrategy(HOMStrategy):
    name = "EACH_CHOICE"

    def generate(self, mutations):
        mutations = mutations[:]
        while mutations:
            mutations_to_apply = []
            available_mutations = mutations[:]
            while len(mutations_to_apply) < self.order and available_mutations:
                try:
                    mutation = available_mutations.pop(0)
                    mutations_to_apply.append(mutation)
                    mutations.remove(mutation)
                except IndexError:
                    break
                self.remove_bad_mutations(mutations_to_apply, available_mutations)
            yield mutations_to_apply


class BetweenOperatorsHOMStrategy(HOMStrategy):
    name = "BETWEEN_OPERATORS"

    def generate(self, mutations):
        usage = {mutation: 0 for mutation in mutations}
        not_used = mutations[:]
        while not_used:
            mutations_to_apply = []
            available_mutations = mutations[:]
            available_mutations.sort(key=lambda x: usage[x])
            while len(mutations_to_apply) < self.order and available_mutations:
                mutation = available_mutations.pop(0)
                mutations_to_apply.append(mutation)
                if not usage[mutation]:
                    not_used.remove(mutation)
                usage[mutation] += 1
                self.remove_bad_mutations(
                    mutations_to_apply, available_mutations, allow_same_operators=False
                )
            yield mutations_to_apply


class RandomHOMStrategy(HOMStrategy):
    name = "RANDOM"

    def __init__(self, *args, shuffler=random.shuffle, **kwargs):
        super().__init__(*args, **kwargs)
        self.shuffler = shuffler

    def generate(self, mutations):
        mutations = mutations[:]
        self.shuffler(mutations)
        while mutations:
            mutations_to_apply = []
            available_mutations = mutations[:]
            while len(mutations_to_apply) < self.order and available_mutations:
                try:
                    mutation = available_mutations.pop(0)
                    mutations_to_apply.append(mutation)
                    mutations.remove(mutation)
                except IndexError:
                    break
                self.remove_bad_mutations(mutations_to_apply, available_mutations)
            yield mutations_to_apply


hom_strategies = [
    BetweenOperatorsHOMStrategy,
    EachChoiceHOMStrategy,
    FirstToLastHOMStrategy,
    RandomHOMStrategy,
]


class FirstOrderMutator:

    def __init__(self, operators, percentage=100):
        self.operators = operators
        self.sampler = utils.RandomSampler(percentage)

    def mutate(self, target_ast, to_mutate=None, coverage_injector=None, module=None):
        # pprint.pprint(ast.dump(target_ast))
        for op in utils.sort_operators(self.operators):
            for mutation, mutant in op().mutate(
                target_ast, to_mutate, self.sampler, coverage_injector, module=module
            ):
                yield [mutation], mutant


class HighOrderMutator(FirstOrderMutator):

    def __init__(self, *args, hom_strategy=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hom_strategy = hom_strategy or FirstToLastHOMStrategy(order=2)

    def mutate(self, target_ast, to_mutate=None, coverage_injector=None, module=None):
        mutations = self.generate_all_mutations(
            coverage_injector, module, target_ast, to_mutate
        )
        for mutations_to_apply in self.hom_strategy.generate(mutations):
            generators = []
            applied_mutations = []
            mutant = target_ast
            for mutation in mutations_to_apply:
                generator = mutation.operator().mutate(
                    mutant,
                    to_mutate=to_mutate,
                    sampler=self.sampler,
                    coverage_injector=coverage_injector,
                    module=module,
                    only_mutation=mutation,
                )
                try:
                    new_mutation, mutant = generator.__next__()
                except StopIteration:
                    assert False, "no mutations!"
                applied_mutations.append(new_mutation)
                generators.append(generator)
            yield applied_mutations, mutant
            self.finish_generators(generators)

    def generate_all_mutations(self, coverage_injector, module, target_ast, to_mutate):
        mutations = []
        for op in utils.sort_operators(self.operators):
            for mutation, _ in op().mutate(
                target_ast, to_mutate, None, coverage_injector, module=module
            ):
                mutations.append(mutation)
        return mutations

    def finish_generators(self, generators):
        for generator in reversed(generators):
            try:
                generator.__next__()
            except StopIteration:
                continue
            assert False, "too many mutations!"
