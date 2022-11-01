from dataclasses import dataclass
from aiopoke.objects.resources import Location
from src.entities.trainer import Trainer

@dataclass
class Gym:
    location: Location
    trainer: Trainer