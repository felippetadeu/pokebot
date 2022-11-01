import aiopoke
import aiopoke.objects.resources as resources
from aiopoke.utils.minimal_resources import MinimalResource

from typing import List, Callable, Dict, Any

def toJSON(o):
    dictionary = o.__dict__
    if type(o) == MinimalResource:
        return {'name': dictionary['name'], 'url': dictionary['url']}
        
    return dictionary

class Teste(resources.Generation):

    def __init__(self, *, id: int, name: str, abilities: List[Dict[str, Any]], main_region: Dict[str, Any], moves: List[Dict[str, Any]], pokemon_species: List[Dict[str, Any]], types: List[Dict[str, Any]], version_groups: List[Dict[str, Any]], names: List[Dict[str, Any]]) -> None:
        super().__init__(id=id, name=name, abilities=abilities, main_region=main_region, moves=moves, pokemon_species=pokemon_species, types=types, version_groups=version_groups, names=names)

class Store:
    pokemons: List[resources.Pokemon] = []
    pokemons_species: List[resources.PokemonSpecies] = []
    generation: resources.Generation = None
    region: resources.Region = None

    @staticmethod
    async def pokemon(pokemon_id: int) -> resources.Pokemon:
        func: Callable[[resources.Pokemon], resources.Pokemon] = lambda p: p.id == pokemon_id
        pokemon = list(filter(func, Store.pokemons))
        if len(pokemon) == 0:
            return await Store.store_pokemon(pokemon_id)
            
        return pokemon[0]

    @staticmethod
    async def store_pokemon(pokemon_id: int) -> resources.Pokemon:
        async with aiopoke.AiopokeClient() as client:
            pokemon = await client.get_pokemon(pokemon_id)
            Store.pokemons.append(pokemon)
            return pokemon

    @staticmethod
    def load_generation(data):
        Store.generation = Teste(**data)
        Store.pokemons_species = Store.generation.pokemon_species

    @staticmethod
    def load_region(data):
        Store.region = resources.Region(**data)

    @staticmethod
    def load_pokemon_species(data):
        Store.pokemons_species.append(resources.PokemonSpecies(**data))

    @staticmethod
    def load_pokemon(data):
        if data['sprites'] is not None:
            for attr in data['sprites']:
                if data['sprites'] is not None and data['sprites'][attr] is not None and 'url' in data['sprites'][attr]:
                    data['sprites'][attr] = data['sprites'][attr]['url']
        Store.pokemons.append(resources.Pokemon(**data))

    @staticmethod
    def save():
        import os
        import json
        for pokemon in Store.pokemons:
            with open(os.path.join('.', 'src', 'data', 'files', 'pokemons', f'{str(pokemon.id)}.json'), 'w') as outfile:
                json.dump(pokemon, outfile, default=lambda o: toJSON(o))

        for specie in Store.pokemons_species:
            with open(os.path.join('.', 'src', 'data', 'files', 'pokemon_species', f'{str(specie.id)}.json'), 'w') as outfile:
                json.dump(specie, outfile, default=lambda o: toJSON(o))

        with open(os.path.join('.', 'src', 'data', 'files', 'generations', f'{str(Store.generation.id)}.json'), 'w') as outfile:
            json.dump(Store.generation, outfile, default=lambda o: toJSON(o))

        with open(os.path.join('.', 'src', 'data', 'files', 'regions', f'{str(Store.region.id)}.json'), 'w') as outfile:
            json.dump(Store.region, outfile, default=lambda o: toJSON(o))