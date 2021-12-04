# Challenge 1 Solution
# async is single-threaded, single-process
import asyncio


async def t1():
    await t2()      # swith next
    print("t1")


async def t2():
    print("t2")


async def t3():
    await t1()      # switch  next
    print("t3")

#  ---t3---no execute_switch---t1--no
# execute_switch---t2------execute----<--------t1--reverse-execute-from-switch---<----t3--reverse-execute-from-switch

asyncio.run(t3())
