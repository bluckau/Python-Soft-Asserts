import sys
from unittest import *
from actions import Actions
import traceback

from typing import (
    Any, Container, Iterable, Optional, Tuple, Union
)


class SoftAsserts:
    def assert_all(self):
        """Process all assertions and clear the slate"""
        count = 0
        msg = "\n\nFailure Details:\n"
        for a in self._exceptions:
            count += 1
            msg += ("Failure #{}:{}\n".format(count, str(a)))
            if hasattr(a, 'stack_trace'):
                msg += str(getattr(a, 'stack_trace'))
                msg += str(a)
        if count > 0:
            msg = msg + "\n{} assertions failed in {}".format(count, self._testMethodName)
            raise AssertionError(msg)

    def _do_assert(self, assert_func, action: Actions = Actions.SOFT_FAIL):
        """
        Run the assert_func and capture the assert unless force
        Differentiated from self.soft_assert because we may want to override _do_assert from other base classes, also
        soft_assert is public facing.
        Puts the assert into a list and run the _on_ actions
        :param assert_func: lambda
        :param force: bool
        :return:
        """

        try:
            assert_func()
        except AssertionError as e:
            setattr(e, "stack_trace", traceback.format_exc())
            self._on_failed_assert(e)
            self._on_assert()
            return False
        else:
            self._on_passed_assert()
            self._on_assert()
            return True

    def soft_assert(self, assert_func, action:Actions = Actions.SOFT_FAIL):
        '''soft_asert any method'''
        self._do_assert(assert_func, action)

    def assertEqual(self, first: Any, second: Any, msg: Any = ..., action = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertEqual(first, second, msg), action)

    def assertNotEqual(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertNotEqual(first, second, msg), action)

    def assertTrue(self, expr: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super(SoftAssertsTestCase, self).assertTrue(expr, msg), action)

    def assertFalse(self, expr: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super(SoftAssertsTestCase, self).assertFalse(expr, msg), action)

    def assertIs(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertIs(first, second, msg), action)

    def assertIsNot(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertIsNot(first, second, msg), action)

    def assertIsNone(self, expr: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super(SoftAssertsTestCase, self).assertNone(expr, msg), action)

    def assertIsNotNone(self, expr: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super(SoftAssertsTestCase, self).assertNotNone(expr, msg), action)

    def assertIn(self, member: Any,
                 container: Union[Iterable[Any], Container[Any]],
                 msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> None:
        return self._do_assert(lambda: super().assertIn(member, container, msg), action)

    def assertNotIn(self, member: Any,
                 container: Union[Iterable[Any], Container[Any]],
                 msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> None:
        return self._do_assert(lambda: super().assertNotIn(member, container, msg), action)


    def assertIsInstance(self, obj: Any,
                         cls: Union[type, Tuple[type, ...]],
                         msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertIsInstance(obj, cls, msg), action)


    def assertNotIsInstance(self, obj: Any,
                         cls: Union[type, Tuple[type, ...]],
                         msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertNotIsInstance(obj, cls, msg), action)

    def assertGreater(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertGreater(first, second, msg), action)

    def assertGreaterEqual(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertGreaterEqual(first, second, msg), action)

    def assertLess(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertLess(first, second, msg), action)

    def assertLessEqual(self, first: Any, second: Any, msg: Any = ..., action: Actions = Actions.SOFT_FAIL) -> bool:
        return self._do_assert(lambda: super().assertLessEqual(first, second, msg), action)




class SoftAssertsTestCase(TestCase, SoftAsserts):
    def setUp(self):
        self._exceptions = []

    def tearDown(self):
        #self.assert_all()
        super().tearDown()

    def run(self, result: Optional[TestResult] = ...) -> TestCase:
        super().run()
        self.assert_all()
        return self

    def _on_assert(self):
        #Actions to do on assert.
        pass

    def _on_assert_all(self):
        #Actions to do on assert_all.
        pass


    def _on_passed_assert(self):
        pass

    def _on_failed_assert(self, e:Exception):
        print("ON ASSERT FAIL ADDING FAILURE")
        self.defaultTestResult().addFailure(self, sys.exc_info())

        # this might not be needed in light of the above line(use the failures logged in defaultTestResult instead)
        self._exceptions.append(e)

        msg = str(e)
        msg_lines = msg.splitlines()