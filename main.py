# import math
#
# def newton_interpolation(x0, h, N, Y, XX, m):
#     # иначе не хватит узлов
#     if N < m + 1:
#         return 0.0, 1
#     x_last = x0 + (N - 1) * h
#     m = int(m)
#     N = int(N)
#     if XX < x0 or XX > x_last:
#         return 0.0, 2
#
#     ideal_p = (XX - x0) / h - m / 2.0
#     p = int(round(ideal_p))
#     p = max(0, min(p, N - 1 - m))
#     print("индекс начала нужных узлов:", p)
#     b = [0.0] * (m + 1)
#     for k in range(m + 1):
#         s = 0.0
#         for i in range(k + 1):
#             sign = (-1) ** (k - i)
#             term = sign * Y[p + i] / (math.factorial(i) * math.factorial(k - i) * (h ** k))
#             s += term
#         b[k] = s
#
#     # Вычисление значения многочлена в точке
#     result = 0.0
#     for k in range(m + 1):
#         prod = 1.0
#         # Вычисляем произведение (XX - t_0)(XX - t_1)...(XX - t_{k-1})
#         for j in range(k):
#             tj = x0 + (p + j) * h   # узел t_j
#             prod *= (XX - tj)
#         result += b[k] * prod
#
#     return result, 0
#
#
# def file_reader(file_name: str):
#     flag = False
#     with open(file_name) as file:
#         for line in file:
#             if flag:
#                 x0, h, XX, N, m, *Y = tuple(float(ch) for ch in line.split())
#                 yield x0, h, XX, N, m, Y
#             else:
#                 flag = True
#
#
# def func1(x: float):
#     return 3*x + 4
#
#
# def func2(x: float):
#     return 4*x**2 + 5*x + 2
#
#
# def main():
#     funcs = (func1, func2)
#     for data, func in zip(file_reader("data"), funcs):
#         print("x0 h XX N m")
#         print(data)
#         x0, h, XX, N, m, Y = data
#         yy, ier = newton_interpolation(x0, h, N, Y, XX, m)
#         if ier == 0:
#             print(f"Приближённое значение: {yy}")
#             print(f"Точное значение: {func(XX)}")
#             print(f"погрешность: {abs(yy - func(XX))}")
#         else:
#             print(f"Ошибка: {ier}")
#         print()
#         Y[0] = 1000
#         print(Y)
#         yy, ier = newton_interpolation(x0, h, N, Y, XX, m)
#         if ier == 0:
#             print(f"Приближённое значение: {yy}")
#             print(f"Точное значение: {func(XX)}")
#             print(f"погрешность: {abs(yy - func(XX))}")
#         else:
#             print(f"Ошибка: {ier}")
#         print("+" * 50)
#
#
# if __name__ == "__main__":
#     main()
#
#
# import requests
#
# access_token = "f9LHodD0cOKxSFOK7daX6Z5Wvvfzh9hwVJK3FA6zAN3nWLAVqrFmX5qTcxiIiCuZrZYbg6HGWuiEhycsBPKi"
# url = f"https://platform-api.max.ru/messages?user_id=51835732"
#
# payload = {
#     "text": "Я использую MAX-API для отправки этого сообщения!",
#     "attachments": [
#         {
#             "type": "reply_keyboard",
#             "payload": {
#                 "buttons": [
#                     [
#                         {
#                             "type": "callback",
#                             "text": "Press me!",
#                             "payload": "button1 pressed"
#                         }
#                     ]
#                 ]
#             }
#         }
#     ]
# }
# headers = {
#     "Authorization": access_token,
#     'Content-Type': 'application/json'
# }
#
# response = requests.post(url, json=payload, headers=headers)
#
# print(response.json())




import time
import requests

API_BASE_URL = "https://platform-api.max.ru"
access_token = "f9LHodD0cOKxSFOK7daX6Z5Wvvfzh9hwVJK3FA6zAN3nWLAVqrFmX5qTcxiIiCuZrZYbg6HGWuiEhycsBPKi"

def get_updates(marker=None):
    url = f"{API_BASE_URL}/updates"
    headers = {
        "Authorization": access_token
    }
    params = {
        "limit": 100,
        "timeout": 3,
        "marker": marker
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=35)
        print("url:",response.url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException as e:
        return None


def process_update(update):
    update_type = update.get('type')

    if update_type == 'message_created':
        message_data = update.get('message', {})
        print(message_data)

if __name__ == "__main__":
    current_marker = None

    while True:
        try:
            print("try get data")
            data = get_updates(marker=current_marker)
            print("data:", data)
            if data and data.get('updates'):
                for update in data['updates']:
                    process_update(update)
                current_marker = data.get('marker')
            else:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Бот остановлен.")
            break
        except Exception as e:
            time.sleep(5)


# import requests
# import time
#
# BOT_TOKEN = "f9LHodD0cOKxSFOK7daX6Z5Wvvfzh9hwVJK3FA6zAN3nWLAVqrFmX5qTcxiIiCuZrZYbg6HGWuiEhycsBPKi"
# user_id = 51835732
# chat_id = -72141646419284
# file_path = "document.xlsx"
#
# upload_response = requests.post(
#     "https://platform-api.max.ru/uploads?type=file",
#     headers={"Authorization": BOT_TOKEN}
# )
# upload_data = upload_response.json()
# upload_url = upload_data["url"]
# print(upload_url)
#
# with open(file_path, "rb") as f:
#     files = {
#         "file": ("document.txt", f, "application/octet-stream")
#     }
#     upload_file_response = requests.post(
#         upload_url,
#         files=files,
#         #headers={"Authorization": BOT_TOKEN}
#     )
#
# upload_result = upload_file_response.json()
# print(upload_result)
# file_token = upload_result["token"]
#
# #time.sleep(10)
#
# message_payload = {
#     "text": "Вот запрошенный документ",
#     # "attachments": [
#     #     {
#     #         "type": "file",
#     #         "payload": {
#     #             "token": file_token
#     #         }
#     #    }
#     # ]
# }
#
# response = requests.post(
#     f"https://platform-api.max.ru/messages?user_id={user_id}",
#     json=message_payload,
#     headers={
#         "Authorization": BOT_TOKEN,
#         "Content-Type": "application/json"
#     }
# )
#
# print(response.json())