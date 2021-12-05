# 1.0.5 Wait for an email reply
import asyncio


async def email_reply():
    await asyncio.sleep(4)
    return f"How you doing?"


async def task1():
    print("Waiting for reply...")
    x = await email_reply()
    print(f"Reply: {x}")

# exec task1--<JMP1>--switch to email_reply()--<JMP2>--NextCoroutine--NoCoroutine-->--No coroutine--<---->exec
# JMP2--->exec JMP1--->done

asyncio.run(task1())
