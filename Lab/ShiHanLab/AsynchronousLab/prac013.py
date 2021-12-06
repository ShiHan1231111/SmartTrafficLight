# 1.0.6 await multiple tasks
import asyncio


async def file_return():
    await asyncio.sleep(1)
    return f"File returned"


async def email_reply():
    await asyncio.sleep(3)
    return f"How you doing?"


async def task1():
    print("Waiting for reply...")
    x = await email_reply()
    print(f"Email Reply: {x}")


async def task2():
    print("Waiting for file...")
    x = await file_return()
    print(f"File returned: {x}")


async def main():
    # await asyncio.gather(task1(),task2())
    # sequence : task1()--switch--->-email()----> NextCoroutine ------>

    # task2()-----switch------->file_return()------NextCoroutine------->None---><------reverse exec <--------file
    # return()<-------->task2()------>rem

    #  <---reverse_exec-------->email()---> task1

    test = asyncio.create_task(task1())
    test2 = asyncio.create_task(task2())

    await test
    await test2


asyncio.run(main())
