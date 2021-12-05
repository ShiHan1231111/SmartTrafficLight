# 1.0.4 Wait for a task
import asyncio
async def task1():
    print("1")
    await asyncio.sleep(1)
    print("2")

asyncio.run(task1())