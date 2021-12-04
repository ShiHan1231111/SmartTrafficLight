# Challenge 2 Solution
import asyncio


async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)          # switch next
    print("Data returned...")
    return {"data": 100}


async def task2():
    for i in range(10):
        print(i)
        await asyncio.sleep(2)      # switch next


async def main():
    x = asyncio.create_task(fetch_data())
    y = asyncio.create_task(task2())

    data = await x                  # no switch
    print(data)
    await y                         # no switch
                                    # no next

asyncio.run(main())
