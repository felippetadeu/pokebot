import numpy as np
from dataclasses import dataclass, field
from typing import List
from src.data.store import Store
from aiopoke.objects.resources import Pokemon as AIOPokemon, Move
from aiopoke.objects.resources.pokemon.pokemon import PokemonMove

@dataclass
class Pokemon():
    id: int
    pokemon: AIOPokemon
    level: int
    exp: int = field(default=0)
    moves: List[PokemonMove] = field(default_factory=list)

    @property
    def level_max_exp(self):
        return self.level * self.level * self.level
    
    def gain_xp(self, exp_amount: int):
        final_exp = self.exp + exp_amount
        if final_exp > self.level_max_exp:
            self.level_up()
            self.gain_xp(final_exp - self.level_max_exp)
        else:
            self.exp = final_exp

    def level_up(self):
        self.level = self.level + 1
        self.learn_move()

    def learn_move(self):
        moves = Pokemon.get_moves_of_level(self.pokemon, self.level)
        learned = False
        iterations = 0
        if len(self.moves) < 4 and len(moves) > 0 and iterations < len(moves) and not learned:
            move = np.random.choice(moves)
            if len(list(filter(lambda x: x.move.name == move.move.name, self.moves))) == 0:
                self.moves.append(move)

    def known_moves(self):
        level = self.level
        moves = []
        while level > 0:
            moves.extend(Pokemon.get_moves_of_level(self.pokemon, level))
            level = level - 1
        return moves

    @staticmethod
    async def create(id: int, starter_level: int = 1):
        stored_pokemon = await Store.pokemon(id)
        moves = []
        level = starter_level
        while level > 0:
            moves.extend(Pokemon.get_moves_of_level(stored_pokemon, level))
            level = level - 1

        starter_moves = []
        if len(moves) < 5:
            starter_moves.extend(moves)
        else:
            while len(starter_moves) < 4:
                move = np.random.choice(moves)
                if len(list(filter(lambda x: x.move.name == move.move.name, starter_moves))) == 0:
                    starter_moves.append(move)
        pokemon = Pokemon(id, stored_pokemon, starter_level, 0, starter_moves)

        return pokemon

    @staticmethod
    def get_moves_of_level(pokemon: AIOPokemon, level: int) -> List[Move]:
        moves = []
        move: PokemonMove
        for move in pokemon.moves:
            min_version = 'red-blue'
            for version in move.version_group_details:
                if version.version_group.name == min_version and version.move_learn_method.name == 'level-up' and version.level_learned_at == level:
                    moves.append(move)
                    break

        return moves
