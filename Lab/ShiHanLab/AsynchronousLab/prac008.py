# 1.0.3 Run with asyncio
import asyncio
async def task1():
    print("Ping")

# Creates event loop
asyncio.run(task1())