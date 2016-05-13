import sys
import unittest

from accessmod import *

class PublicDecoratorTest(unittest.TestCase):
    def test_method_no_args(self):
        class TestClass:
            @public
            def method1(self):
                return 1
        tc = TestClass()
        self.assertEqual(tc.method1(), 1)
        return
    def test_method_multiple_args(self):
        class TestClass:
            @public
            def method1(self, a, b, c, d):
                return [a, b, c, d]
        tc = TestClass()
        test_list = [1, 2, 3, 4]
        self.assertListEqual(tc.method1(*test_list), test_list)
        return
    def test_static_method(self):
        class TestClass:
            @staticmethod
            @public
            def method1():
                return 1
        self.assertEqual(TestClass.method1(), 1)
        return
    def test_classmethod(self):
        class TestClass:
            value = 1
            @classmethod
            @public
            def method1(cls):
                return cls.value
        self.assertEqual(TestClass.method1(), 1)
        return

class PrivateDecoratorTest(unittest.TestCase):
    def test_method_no_args(self):
        class TestClass:
            @private
            def method1(self):
                return 1
            def method2(self):
                return self.method1()
        tc = TestClass()
        try:
            self.assertEqual(tc.method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up but It should have not. ({0})".format(err))
        return
    def test_method_multiple_args(self):
        class TestClass:
            @private
            def method1(self, a, b, c, d):
                return [a, b, c, d]
            def method2(self, a, b, c, d):
                return self.method1(a, b, c, d)
        tc = TestClass()
        test_list = [1, 2, 3, 4]
        try:
            self.assertListEqual(tc.method2(*test_list), test_list)
        except AttributeError as err:
            self.fail("Exception showed up but It should have not. ({0})".format(err))
        return
    def test_static_method(self):
        class TestClass:
            @staticmethod
            @private
            def method1():
                return 1
            def method2(self):
                return self.method1()
        try:
            self.assertEqual(TestClass().method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up but It should have not. ({0})".format(err))
        return
    def test_classmethod(self):
        class TestClass:
            value = 1
            @classmethod
            @private
            def method1(cls):
                return cls.value
            def method2(self):
                return TestClass.method1()
        try:
            self.assertEqual(TestClass().method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up: {0}".format(err))
        return
    def test_outer_call(self):
        class TestClass:
            @private
            def method1(self):
                return
        tc = TestClass()
        with self.assertRaises(AttributeError) as context:
            tc.method1()
        self.assertTrue("only accessible from" in str(context.exception))
        return

    def test_inheritance(self):
        class TestClassBase:
            @private
            def method1(self):
                return
        class TestClassChild(TestClassBase):
            def method2(self):
                return self.method1()

        tc = TestClassChild()
        with self.assertRaises(AttributeError) as context:
            tc.method2()
        self.assertTrue("only accessible from" in str(context.exception))
        return

class ProtectedDecoratorTest(unittest.TestCase):
    def test_method_no_args(self):
        class TestClass:
            @protected
            def method1(self):
                return 1
            def method2(self):
                return self.method1()
        tc = TestClass()
        try:
            self.assertEqual(tc.method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up but It should have not. ({0})".format(err))
        return
    def test_method_multiple_args(self):
        class TestClass:
            @protected
            def method1(self, a, b, c, d):
                return [a, b, c, d]
            def method2(self, a, b, c, d):
                return self.method1(a, b, c, d)
        tc = TestClass()
        test_list = [1, 2, 3, 4]
        try:
            self.assertListEqual(tc.method2(*test_list), test_list)
        except AttributeError as err:
            self.fail("Exception showed up but It should have not. ({0})".format(err))
        return
    def test_static_method(self):
        class TestClass:
            @staticmethod
            @protected
            def method1():
                return 1
            def method2(self):
                return self.method1()
        try:
            self.assertEqual(TestClass().method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up but It should have not. ({0})".format(err))
        return
    def test_classmethod(self):
        class TestClass:
            value = 1
            @classmethod
            @protected
            def method1(cls):
                return cls.value
            def method2(self):
                return TestClass.method1()
        try:
            self.assertEqual(TestClass().method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up: {0}".format(err))
        return
    def test_outer_call(self):
        class TestClass:
            @protected
            def method1(self):
                return
        tc = TestClass()
        with self.assertRaises(AttributeError) as context:
            tc.method1()
        self.assertTrue("only accessible from" in str(context.exception))
        return

    def test_inheritance(self):
        class TestClassBase:
            @protected
            def method1(self):
                return 1
        class TestClassChild(TestClassBase):
            def method2(self):
                return self.method1()
        try:
            self.assertEqual(TestClassChild().method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up: {0}".format(err))
        return

    def test_child_class_visibility(self):
        class TestClassBase1:
            pass
        class TestClassBase2:
            pass
        class TestClassBase3:
            @protected
            def method1(self):
                return 1
        class TestClassChild(TestClassBase1, TestClassBase2, TestClassBase3):
            def method2(self):
                return self.method1()
        try:
            self.assertEqual(TestClassChild().method2(), 1)
        except AttributeError as err:
            self.fail("Exception showed up: {0}".format(err))
        return

if __name__ == '__main__':
    sys.exit(unittest.main())
