import aiopoke
import os
import json
from src.data.store import Store

class Setup:

    @staticmethod
    async def start(force_reload: bool = False):
        if force_reload:
            await Setup.load_species(1)
            await Setup.load_pokemons()
            Setup.store_data()
        else:
            Setup.load_stored_data()

    @staticmethod
    async def load_species(generation_id: int):
        async with aiopoke.AiopokeClient() as client:
            Store.generation = await client.get_generation(generation_id)
            Store.region = await client.get_region(generation_id)
            for specie in Store.generation.pokemon_species:
                Store.pokemons_species.append(await client.get_pokemon_species(specie.name))

    @staticmethod
    async def load_pokemons():
        for poke_specie in Store.pokemons_species:
            print(f'Loading.... {poke_specie.id}')
            await Store.pokemon(poke_specie.id)

    @staticmethod
    def store_data():
        Store.save()        

    @staticmethod
    def load_stored_data():
        root_path = os.path.join('.', 'src', 'data', 'files')
        
        entries = os.scandir(os.path.join(root_path, 'generations'))
        for entry in entries:
            with open(entry) as file:
                Store.load_generation(json.loads(file.read()))
        
        entries = os.scandir(os.path.join(root_path, 'pokemon_species'))
        for entry in entries:
            with open(entry) as file:
                Store.load_pokemon_species(json.loads(file.read()))
        
        entries = os.scandir(os.path.join(root_path, 'pokemons'))
        for entry in entries:
            with open(entry) as file:
                Store.load_pokemon(json.loads(file.read()))
        
        entries = os.scandir(os.path.join(root_path, 'regions'))
        for entry in entries:
            with open(entry) as file:
                Store.load_region(json.loads(file.read()))