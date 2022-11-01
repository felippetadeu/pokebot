import asyncio
from pickle import TRUE
from src.setup import Setup
from src.data.store import Store
from src.entities.trainer import Trainer

async def main():
    await Setup.start(True)

    trainer = await Trainer.create('18304u1=123-41234', 'Felippe', 4)
    trainer.pokemons[0].gain_xp(5000)
    print(trainer)

if __name__ == '__main__':
    asyncio.run(main())