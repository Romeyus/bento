import threading
import time
from collections.abc import Generator
from dataclasses import dataclass

import pytest

from bento import Singleton

# ==========================================
# ===            Constants               ===
# ==========================================
NB_THREADS = 20


# ==========================================
# ===            Mocks                   ===
# ==========================================
@dataclass(frozen=True, slots=True)
class MockSingletonA(Singleton):
    value: str


class MockSingletonB(Singleton): ...


# ==========================================
# ===            Fixtures                ===
# ==========================================
@pytest.fixture(autouse=True)
def clear_singleton_instances() -> Generator[None]:
    Singleton.__clear__()
    yield


# ==========================================
# ===            Lifetimes               ===
# ==========================================
class TestSingleton:
    def test_singleton_should_return_same_instance(self) -> None:
        instance1 = MockSingletonB()
        instance2 = MockSingletonB()
        assert instance1 is instance2

    def test_singleton_should_return_different_instances_for_different_classes(
        self,
    ) -> None:
        a = MockSingletonA("A")
        b = MockSingletonB()
        assert a is not b

    def test_singleton_should_ignore_args_after_first_call(self) -> None:
        MockSingletonA("First")
        second = MockSingletonA("Second")
        assert second.value == "First"

    def test_singleton_should_be_thread_safe(self) -> None:
        class ThreadedSingleton(Singleton):
            def __init__(self) -> None:
                time.sleep(0.1)

        barrier = threading.Barrier(NB_THREADS)
        instances: list[ThreadedSingleton] = []

        def create_instance() -> None:
            barrier.wait()
            instances.append(ThreadedSingleton())

        threads: list[threading.Thread] = []
        for _ in range(NB_THREADS):
            threads.append(threading.Thread(target=create_instance))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        first_instance = instances[0]
        assert all(inst is first_instance for inst in instances)
