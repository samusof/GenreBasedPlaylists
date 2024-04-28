from typing import Optional
from unittest import TestCase

from instance_providers.singleton import Singleton


class ClassToTest(metaclass=Singleton):
    def __init__(self, value: Optional[int] = None):
        self.value = value


class TestSingleton(TestCase):

    def test_given_multiple_instantiations_of_class_should_return_same_object(self):
        object1 = ClassToTest()
        object2 = ClassToTest()
        assert object1 is object2

    def test_give_multiple_instantiations_of_class_should_not_overwrite_data(self):
        object1 = ClassToTest(10)
        object2 = ClassToTest(900)
        assert object2.value == 10
