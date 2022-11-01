from dataclasses import dataclass
from typing import List
from src.entities.world import World

@dataclass
class Bot:
    worlds: List[World] = []

    async def create_world(self, id: str):
        world: World = World(id)
        await world.start_world()
        self.add_world(world)

    def add_world(self, world: World):
        Bot.worlds.append(world)