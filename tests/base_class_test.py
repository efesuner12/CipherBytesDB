def compute_shared_values(dependent_value):
    shared_value_result = 10 * dependent_value
    shared_string_result = "Hello" + str(dependent_value)
    
    return shared_value_result, shared_string_result

class BaseClass:
    CONSTANT = ""

    @classmethod
    def initialize_shared_values(cls):
        cls.shared_value, cls.shared_string = compute_shared_values(cls.CONSTANT)

    def __init__(self):
        pass

class Subclass1(BaseClass):
    def __init__(self, name):
        super().__init__()
        self.name = name

class Subclass2(BaseClass):
    def __init__(self, value):
        super().__init__()
        self.value = value


if __name__ == "__main__":
    BaseClass.CONSTANT = 5
    BaseClass.initialize_shared_values()

    subclass1_instance = Subclass1("Subclass1")
    subclass2_instance = Subclass2(20)

    print(subclass1_instance.shared_value)  # Output: 50

    print(subclass2_instance.shared_string)  # Output: Hello5
