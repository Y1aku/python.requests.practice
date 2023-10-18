import requests
import asyncio
import aiohttp
from config_log import to_log
from config_data import config


def authorise():  # Авторизоваться
    authorise_response = requests.post(config.url + "api/login_check", json=config.auth_payload)
    data = authorise_response.json()
    config.token = data["response"]["token"]
    to_log.do_logs(authorise_response)
    return authorise_response


authorise()

headers = {
    "Authorization": f"Bearer {config.token}"
}

group_id = None
player_id = None


async def create_group():  # Создать группу
    async with aiohttp.ClientSession() as session:
        create_group_response = await session.post(config.url + "api/v1/media_group",
                                                   headers=headers,
                                                   json=config.group_payload)
        await to_log.do_logs_async(create_group_response)
    return create_group_response


async def create_player():  # Создать плеер
    async with aiohttp.ClientSession() as session:
        create_player_response = await session.post(config.url + "api/v1/media_player",
                                                    headers=headers,
                                                    json=config.player_payload)
        await to_log.do_logs_async(create_player_response)
    return create_player_response


async def creating():
    group_response, player_response = await asyncio.gather(create_group(), create_player())
    group_data = await group_response.json()
    player_data = await player_response.json()

    group_id = group_data['response']['id']
    player_id = player_data['response']['id']

    print("Response from create_group:")  # TODO Отладочный код – удалить
    print(group_data)

    print("Response from create_player:")
    print(player_data)

    print(f"group_id: {group_id}")
    print(f"player_id: {player_id}")

    return group_id, player_id

result = asyncio.run(creating())
group_id, player_id = result


def player_to_group():  # Добавить плеер в группу
    player_to_group_response = requests.patch(config.url + f"api/v1/media_player?id={player_id}",
                                            headers=headers,
                                            json={"mediaGroup": group_id})

    if player_to_group_response.status_code == 204:  # TODO Отладочный код – удалить
        # 204 No Content означает успешное выполнение без возврата данных
        print("Update successful")
    elif player_to_group_response.status_code == 200:
        # 200 OK означает успешное выполнение с возвратом данных (JSON, XML и т. д.)
        print("Update successful")
        data = player_to_group_response.json()
        print(data)
    else:
        print(f"Update failed with status code {player_to_group_response.status_code}")

    data = player_to_group_response.json()
    print(data)
    to_log.do_logs(player_to_group_response)
    return player_to_group_response


player_to_group()
'''
'''

# Удалить плеер и группу

async def delete_group():  # Удалить группу
    async with aiohttp.ClientSession() as session:
        delete_group_response = await session.delete(config.url + f"api/v1/media_group?id={group_id}",
                                                   headers=headers)
        await to_log.do_logs_async(delete_group_response)
    return delete_group_response


async def delete_player():  # Удалить плеер
    async with aiohttp.ClientSession() as session:
        delete_player_response = await session.delete(config.url + f"api/v1/media_player?id={player_id}",
                                                    headers=headers)
        await to_log.do_logs_async(delete_player_response)
    return delete_player_response

async def deleting():
    group_response, player_response = await asyncio.gather(delete_group(), delete_player())
    group_data = await group_response.json()  # TODO Отладочный код – удалить
    player_data = await player_response.json()

    print("Response from create_group:")
    print(group_data)

    print("Response from create_player:")
    print(player_data)


asyncio.run(deleting())

