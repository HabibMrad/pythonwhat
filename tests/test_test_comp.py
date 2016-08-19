import unittest
import unittest
import helper


class TestListCompStepByStep(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}",
            "DC_SOLUTION": "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]",
            "DC_SCT": '''
test_list_comp(index=1,
               not_called_msg=None,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               incorrect_iter_vars_msg=None,
               body=lambda: test_expression_result(context_vals = ['a', 2]),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])],
               insufficient_ifs_msg=None,
               expand_message=True)
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the first list comprehension you defined but hasn't found it.")

    def test_fail_2(self):
        self.data["DC_CODE"] = "[key for key in x.keys()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the iterable part of the first list comprehension.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 17, 24)

    def test_fail_3(self):
        self.data["DC_CODE"] = "[a + str(b) for a,b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you used the correct iterator variables in the first list comprehension? Make sure you use the correct names!")
        helper.test_lines(self, sct_payload, 1, 1, 17, 19)

    def test_fail_4(self):
        self.data["DC_CODE"] = "[key + '_' + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertIn("Check your code in the body of the first list comprehension.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 2, 21)

    def test_fail_5(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you used 2 ifs inside the first list comprehension?", sct_payload['message'])
        # helper.test_lines(self, sct_payload, 1, 1, 2, 41) # small hiccup!

    def test_fail_6(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the first if of the first list comprehension. Have you called <code>isinstance()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 45, 64)

    def test_fail_7(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the second if of the first list comprehension. Have you called <code>isinstance()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 69, 88)

    def test_fail_8(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the second if of the first list comprehension. Did you call <code>isinstance()</code> with the correct arguments?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 80, 82)

    def test_pass(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestListCompStepByStepCustom(unittest.TestCase):

    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}",
            "DC_SOLUTION": "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int)]",
            "DC_SCT": '''
test_list_comp(index=1,
               not_called_msg='notcalled',
               comp_iter=lambda: test_expression_result(incorrect_msg = 'iterincorrect'),
               iter_vars_names=True,
               incorrect_iter_vars_msg='incorrectitervars',
               body=lambda: test_expression_result(context_vals = ['a', 2], incorrect_msg = 'bodyincorrect'),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled1', incorrect_msg = 'incorrect2'),
                    lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False], not_called_msg = 'notcalled2', incorrect_msg = 'incorrect2')],
               insufficient_ifs_msg='insufficientifs')
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "notcalled")

    def test_fail_2(self):
        self.data["DC_CODE"] = "[key for key in x.keys()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the iterable part of the first list comprehension. iterincorrect", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 17, 24)

    def test_fail_3(self):
        self.data["DC_CODE"] = "[a + str(b) for a,b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "incorrectitervars")
        helper.test_lines(self, sct_payload, 1, 1, 17, 19)

    def test_fail_4(self):
        self.data["DC_CODE"] = "[key + '_' + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertIn("Check your code in the body of the first list comprehension. bodyincorrect", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 2, 21)

    def test_fail_5(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("insufficientifs", sct_payload['message'])
        # helper.test_lines(self, sct_payload, 1, 1, 2, 41) # small hiccup!

    def test_fail_6(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the first if of the first list comprehension. notcalled1", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 45, 64)

    def test_fail_7(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test')]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the second if of the first list comprehension. notcalled2", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 69, 88)

    def test_fail_8(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str)]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the second if of the first list comprehension. incorrect2", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 80, 82)

    def test_pass(self):
        self.data["DC_CODE"] = "[key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str)]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])


class TestListCompNested(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "",
            "DC_SOLUTION": "[[col for col in range(5)] for row in range(5)]",
            "DC_SCT": "test_list_comp(1, body = lambda: test_list_comp(1, body = lambda: test_expression_result(context_vals = [4])))"
        }

    def test_fail(self):
        self.data["DC_CODE"] = "[[col + 1 for col in range(5)] for row in range(5)]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])

    def test_pass(self):
        self.data["DC_CODE"] = "[[col for col in range(5)] for row in range(5)]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestListIterVars(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a':1, 'b':2}",
            "DC_SOLUTION": "[key for key, value in x.items()]",
            "DC_SCT": "test_list_comp(1, iter_vars_names=False)"
        }

    def test_fail(self):
        self.data["DC_CODE"] = "[a for a in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you used 2 iterator variables in the first list comprehension?")

    def test_pass(self):
        self.data["DC_CODE"] = "[a for a,b in x.items()]"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

class TestDictCompStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "lst = ['this', 'is', 'a', 'list']",
            "DC_SOLUTION": "{ el:len(el) for el in lst if isinstance(el, str)}",
            "DC_SCT": '''
test_dict_comp(index=1,
               not_called_msg=None,
               comp_iter=lambda: test_expression_result(),
               iter_vars_names=True,
               incorrect_iter_vars_msg=None,
               key=lambda: test_expression_result(context_vals = ['a']),
               value=lambda: test_expression_result(context_vals = ['a']),
               ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])],
               insufficient_ifs_msg=None,
               expand_message=True)
            '''
        }
        self.file = open('output.txt', 'a')

    def tearDown(self):
        self.file.write("\n\n")
        self.file.close()

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("The system wants to check the first dictionary comprehension you defined but hasn't found it.", sct_payload['message'])
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_fail_2(self):
        self.data["DC_CODE"] = "{ a:a for a in lst[1:2] }"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the iterable part of the first dictionary comprehension", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 16, 23)
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_fail_3(self):
        self.data["DC_CODE"] = "{ a:a for a in lst }"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you used the correct iterator variables in the first dictionary comprehension? Make sure you use the correct names!", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 11, 11)
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_fail_4(self):
        self.data["DC_CODE"] = "{ el + 'a':str(el) for el in lst }"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the key part of the first dictionary comprehension.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 3, 10)
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_fail_5(self):
        self.data["DC_CODE"] = "{ el:str(el) for el in lst }"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the value part of the first dictionary comprehension.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 6, 12)
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_fail_6(self):
        self.data["DC_CODE"] = "{ el:len(el) for el in lst }"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you used 1 ifs inside the first dictionary comprehension?", sct_payload['message'])
        # helper.test_lines(self, sct_payload, 1, 1, 6, 12) - small hiccup
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_fail_7(self):
        self.data["DC_CODE"] = "{ el:len(el) for el in lst if isinstance('a', str)}"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the first if of the first dictionary comprehension. Did you call <code>isinstance()</code> with the correct arguments?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 42, 44)
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))

    def test_pass(self):
        self.data["DC_CODE"] = "{ el:len(el) for el in lst if isinstance(el, str)}"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])
        self.file.write("submission: %s\nfeedback: \"%s\"" % (self.data["DC_CODE"], sct_payload["message"]))


class TestGeneratorFunctionStepByStep(unittest.TestCase):
    def setUp(self):
        self.data = {
            "DC_PEC": "x = {'a': 2, 'b':3, 'c':4, 'd':'test'}",
            "DC_SOLUTION": "(key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, int))",
            "DC_SCT": '''
test_generator_exp(index=1,
                   not_called_msg=None,
                   comp_iter=lambda: test_expression_result(),
                   iter_vars_names=True,
                   incorrect_iter_vars_msg=None,
                   body=lambda: test_expression_result(context_vals = ['a', 2]),
                   ifs=[lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False]),
                        lambda: test_function_v2('isinstance', params = ['obj'], do_eval = [False])],
                   insufficient_ifs_msg=None,
                   expand_message=True)
            '''
        }

    def test_fail_1(self):
        self.data["DC_CODE"] = ""
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "The system wants to check the first generator expression you defined but hasn't found it.")

    def test_fail_2(self):
        self.data["DC_CODE"] = "(key for key in x.keys())"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertIn("Check your code in the iterable part of the first generator expression.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 17, 24)

    def test_fail_3(self):
        self.data["DC_CODE"] = "(a + str(b) for a,b in x.items())"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual(sct_payload['message'], "Have you used the correct iterator variables in the first generator expression? Make sure you use the correct names!")
        helper.test_lines(self, sct_payload, 1, 1, 17, 19)

    def test_fail_4(self):
        self.data["DC_CODE"] = "(key + '_' + str(val) for key,val in x.items())"
        sct_payload = helper.run(self.data)
        self.assertIn("Check your code in the body of the first generator expression.", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 2, 21)

    def test_fail_5(self):
        self.data["DC_CODE"] = "(key + str(val) for key,val in x.items())"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Have you used 2 ifs inside the first generator expression?", sct_payload['message'])
        # helper.test_lines(self, sct_payload, 1, 1, 2, 41) # small hiccup!

    def test_fail_6(self):
        self.data["DC_CODE"] = "(key + str(val) for key,val in x.items() if hasattr(key, 'test') if hasattr(key, 'test'))"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the first if of the first generator expression. Have you called <code>isinstance()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 45, 64)

    def test_fail_7(self):
        self.data["DC_CODE"] = "(key + str(val) for key,val in x.items() if isinstance(key, str) if hasattr(key, 'test'))"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the second if of the first generator expression. Have you called <code>isinstance()</code>?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 69, 88)

    def test_fail_8(self):
        self.data["DC_CODE"] = "(key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(key, str))"
        sct_payload = helper.run(self.data)
        self.assertFalse(sct_payload['correct'])
        self.assertEqual("Check your code in the second if of the first generator expression. Did you call <code>isinstance()</code> with the correct arguments?", sct_payload['message'])
        helper.test_lines(self, sct_payload, 1, 1, 80, 82)

    def test_pass(self):
        self.data["DC_CODE"] = "(key + str(val) for key,val in x.items() if isinstance(key, str) if isinstance(val, str))"
        sct_payload = helper.run(self.data)
        self.assertTrue(sct_payload['correct'])

if __name__ == "__main__":
     unittest.main()

# import ast
# from pythonwhat import utils_ast

# code = "[key + str(val) for key,val in x.items()]"
# res = ast.parse(code)
# utils_ast.mark_text_ranges(res, code, debug = True)
# print(ast.dump(res))

