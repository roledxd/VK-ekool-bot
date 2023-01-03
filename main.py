import requests
import commands as cmd
import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton


def main():
    vk_session = vk_api.VkApi(
        token='eb72d458ce4bdfbfea6913d81144e2cbd62558df5d9918613b303ffe40bef7bb1a55085f1ffdf89476d16', api_version="5.120")
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=201949992)

    CALLBACK_TYPES = ("show_snackbar", "open_link", "open_app")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            try:
                resp = cmd.processCommand(event)
                if resp["error"] is not None:
                    vk.messages.send(user_id=event.obj.message["from_id"], random_id=get_random_id(),
                                     message="⚠️ " + resp["error"])
                else:
                    keyboard = None
                    if resp['keyboard'] is not None:
                        keyboard = resp['keyboard']
                    vk.messages.send(user_id=event.obj.message["from_id"], random_id=get_random_id(),
                                     message=resp["response"], keyboard=keyboard)
            except Exception as e:
                vk.messages.send(user_id=event.obj.message["from_id"], random_id=get_random_id(),
                                 message="⚠️ Что-то пошло не так.", keyboard=None)

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get("type") in CALLBACK_TYPES:
                vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload),
                )
            else:
                event_type = event.object.payload.get("type")
                if event_type == "delete_msg":
                    try:
                        msgs = vk.messages.getByConversationMessageId(peer_id=event.object.peer_id, conversation_message_ids=[event.object.conversation_message_id])
                        if len(msgs['items']) != 0:
                            msg = msgs['items'][0]
                            vk.messages.delete(user_id=event.object.user_id, peer_id=event.object.peer_id, message_ids=[msg['id']], random_id=get_random_id(), delete_for_all=True)
                            vk.messages.sendMessageEventAnswer(
                                event_id=event.object.event_id,
                                user_id=event.object.user_id,
                                peer_id=event.object.peer_id,
                                event_data=json.dumps({"type": "show_snackbar", "text": "✔️ Команда выполнена."}),
                            )
                    except Exception as e:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps(
                                {"type": "show_snackbar", "text": "⚠️ Ошибка при исполнении команды."}),
                        )
                else:
                    resp = cmd.processCommand(event, isBotEventType=True)
                    if resp["error"] is not None:
                        vk.messages.send(user_id=event.object.user_id, random_id=get_random_id(), message="⚠️ " + resp["error"])
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "⚠️ Ошибка при исполнении команды."}),
                        )
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "✔️ Команда выполнена."}),
                        )
                        keyboard = None
                        if resp['keyboard'] is not None:
                            keyboard = resp['keyboard']
                        #vk.messages.edit(user_id=event.object.user_id, peer_id=event.object.peer_id, conversation_message_id=event.object.conversation_message_id, random_id=get_random_id(), message=resp["response"],keyboard=keyboard)
                        vk.messages.send(user_id=event.object.user_id, peer_id=event.object.peer_id, conversation_message_id=event.object.conversation_message_id, random_id=get_random_id(), message=resp["response"],keyboard=keyboard)


if __name__ == '__main__':
    main()
