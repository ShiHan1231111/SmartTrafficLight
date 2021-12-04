# 1.0.2 Determine if a function is a coroutine or not
import asyncio


async def task1():
    pass


print(asyncio.iscoroutinefunction(task1))

# asyncio.iscoroutinefunction(func)
# asyncio.iscoroutine(obj)