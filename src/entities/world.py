from dataclasses import dataclass, field
from typing import List

from src.data.store import Store
from .trainer import Trainer
from .map import Map


@dataclass
class World:

    id: str = field()
    region_map: Map = field(default=None)
    trainers: List[Trainer] = field(default_factory=list, init=False)

    async def start_world(self):
        self.map = await Map.generate_map(1)

    def add_trainer(self, trainer: Trainer):
        self.trainers.append(trainer)