# Introduction Example
# synchronous
def task1():
    print('Send first Email')
    print('First Email reply')
    task2()


def task2():
    print('Send second Email')
    print('Second Email reply')
    task3()


def task3():
    print('Send third Email')
    print('Third Email reply')
    print("====")
    print("END")


task1()

# asynchronous

import asyncio


async def task1():
    print('Send first Email')
    asyncio.create_task(task2())
    await asyncio.sleep(2)  # Simulating that the email reply takes 2 seconds
    print('First Email reply')


async def task2():
    print('Send second Email')
    asyncio.create_task(task3())
    await asyncio.sleep(2)
    print('Second Email reply')


async def task3():
    print('Send third Email')
    await asyncio.sleep(2)
    print('Third Email reply')


asyncio.run(task1())
