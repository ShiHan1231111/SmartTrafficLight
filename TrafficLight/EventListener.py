from ComponentSimulation.Firebase import Firebase

fb = Firebase()


class EventListener:
    @staticmethod
    async def listen_switch_event(TRAFFIC_ID):
        switch_instruction = await listen_switch(TRAFFIC_ID)
        return switch_instruction


async def listen_switch(TRAFFIC_ID):
    return fb.read_one(f"Server/Event/Switch/{TRAFFIC_ID}")
