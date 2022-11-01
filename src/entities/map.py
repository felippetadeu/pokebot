from dataclasses import dataclass, field
from typing import List

import aiopoke
from aiopoke.objects.resources.locations.location import Region, Location
from .gym import Gym
from src.data.store import Store

@dataclass
class Map:
    region_id: int
    region: Region
    locations: List[Location] = field(default_factory=list)
    gyms: List[Gym] = field(default_factory=list)

    @staticmethod
    async def generate_map(region_id: int):
        async with aiopoke.AiopokeClient() as client:
            Store.region = await client.get_region(region_id)
            m = Map(region_id, Store.region, Store.region.locations) 
            return m