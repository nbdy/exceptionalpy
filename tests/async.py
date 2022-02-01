import asyncio
from exceptionalpy import exceptionalpy_handler as handler
from exceptionalpy import ex


@ex()
async def x():
    v = None
    v[9] = 52


if __name__ == '__main__':
    handler.verbose = True
    handler.init()

    asyncio.run(x())
