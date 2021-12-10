from Firebase import Firebase

fb = Firebase()


class EventAck(object):
    @staticmethod
    async def ack_switch_event(TL_ID):
        await EventAck.send_switch_ack(TL_ID)

    @staticmethod
    async def send_switch_ack(TL_ID):
        fb.update("Server/Event/Switch", {TL_ID: "SWITCH ACK"})
