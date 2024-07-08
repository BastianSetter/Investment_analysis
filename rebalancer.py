import numpy as np
from abc import ABC, abstractmethod

class Rebalancer(ABC):
    def __init__(self) -> None:
        pass


class TimeRebalancer(Rebalancer):
    def __init__(self) -> None:
        super().__init__()

class DeviationRebalancer(Rebalancer):
    def __init__(self) -> None:
        super().__init__()