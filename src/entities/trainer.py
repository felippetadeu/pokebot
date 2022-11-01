from dataclasses import dataclass, field
from typing import List
from aiopoke.objects.resources import Location
from .pokemon import Pokemon
from src.data.store import Store

@dataclass
class Trainer:

    id: str = None
    name: str = None
    location: Location = field(default=None)
    pokemons: List[Pokemon] = field(default_factory=list)

    @staticmethod
    async def create(id: str, name: str, starter_pokemon_id: int):
        trainer = Trainer(id, name)
        trainer.pokemons.append(await Pokemon.create(starter_pokemon_id, 5))
        return trainer