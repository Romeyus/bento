from bento import SingletonMeta


# ==========================================
# ===            Mocks                   ===
# ==========================================
class MockSingleton(metaclass=SingletonMeta): ...


# ==========================================
# ===            Lifetimes               ===
# ==========================================
class TestSingleton:
    def test_singleton_should_return_same_instance(self) -> None:
        assert MockSingleton() is MockSingleton()

    def test_singleton_is_instance_of_self(self) -> None:
        instance = MockSingleton()
        assert isinstance(instance, MockSingleton)
