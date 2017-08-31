# -*- coding: utf-8 -*-
import sys
from time import sleep

import json
import requests

if sys.version_info < (3,):
	def u(x):
		try:
			return x.encode("utf8")
		except UnicodeDecodeError:
			return x
else:
	def u(x):
		if type(x) == type(b''):
			return x.decode('utf8')
		else:
			return x

# --- Настройки ---
# Вывод отладочной информации
debug = True

# Массив интервалов задержек
delays = [360, 540, 720, 900, 1080]

# Ошибка "Недостаточно баллов"
notEnoughUnitsError = "152"

# --- Входные данные запроса ---
# Адрес сервиса Campaigns для отправки JSON-запросов (регистрозависимый)
CampaignsURL = 'https://api.direct.yandex.com/json/v5/campaigns'

# OAuth-токен пользователя, от имени которого будут выполняться запросы
token = 'ТОКЕН'

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = 'ЛОГИН_КЛИЕНТА'

# --- Подготовка запроса ---
# Создание HTTP-заголовков запроса
headers = {
	"Authorization": "Bearer " + token,     # OAuth-токен. Использование слова Bearer обязательно
	"Client-Login": clientLogin,            # Логин клиента рекламного агентства
	"Accept-Language": "ru",                # Язык ответных сообщений
}

# Создание тела запроса
body = {
	"method": "get",                        # Используемый метод
	"params": {
		"SelectionCriteria": {},            # Критерий отбора кампаний. Для получения всех кампаний должен быть пустым
		"FieldNames": ["Id", "Name"]        # Имена параметров, которые требуется получить
	}
}

# Преобразование входных параметров запроса в формат JSON
jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

# --- Выполнение задачи ---
# Запуск цикла для выполнения запросов. Если первый запрос завершен успешно, т.е. не привел к возникновению ошибки 152,
# то выводится список кампаний.
# Если же первый запрос завершен с этой ошибкой, то выполняются повторные запросы с задержками,
# заданными в массиве delays.
for delay in delays:
	try:
		# Выполнение запроса, получение результата
		result = requests.post(CampaignsURL, jsonBody, headers=headers)

		# Отладочная инфомрация
		if debug:
			print("Заголовки запроса: {}".format(result.request.headers))
			print("Запрос: {}".format(u(result.request.body)))
			print("Заголовки ответа: {}".format(result.headers))
			print("Ответ: {}".format(u(result.text)))
			print("\n")

		# Обработка запроса
		if result.status_code == 200:
			# Если получен HTTP-код 200, то обрабатываем тело ответа

			# Вывод RequestId запроса и информации о баллах
			print("RequestId запроса: {}".format(result.headers.get("RequestId", False)))
			print("Информация о баллах: {}".format(result.headers.get("Units", False)))

			# Если в результирующих данных не содержится первичного ключа error, значит, запрос был выполнен успешно
			if not result.json().get("error", False):
				# Вывод списка кампаний
				for campaign in result.json()["result"]["Campaigns"]:
					print("Рекламная кампания: {} №{}".format(u(campaign['Name']), campaign['Id']))

				# Если ответ содержит параметр LimitedBy, значит, были получены не все доступные объекты.
				if result.json()['result'].get('LimitedBy', False):
					# В этом случае следует выполнить дополнительные запросы для получения всех объектов.
					# Подробное описание постраничной выборки - https://tech.yandex.ru/direct/doc/dg/best-practice/get-docpage/#page
					print("Получены не все доступные объекты.")

				# Принудительный выход из цикла
				break

			# Обработка ошибок запроса к серверу API Директа
			elif result.json().get("error", False):
				print("Произошла ошибка при обращении к серверу API Директа.")
				print("Код ошибки: {}".format(result.json()["error"]["error_code"]))
				print("Описание ошибки: {}".format(u(result.json()["error"]["error_detail"])))
				if result.json()['error'].get('error_code', 0) == notEnoughUnitsError:
					# Недостаточно баллов для выполнения запроса
					print("Повторный запрос через {} секунд".format(delay))
					# Задержка перед выполнением следующего запроса
					sleep(delay)

		# Обработка других ошибок
		else:
			print("Произошла ошибка при обращении к серверу API Директа.")
			print("HTTP-код ошибки: {}".format(u(result.status_code)))
			# Здесь вы можете описать действия, которые следует выполнить при возникновении ошибки HTTP-запроса

	# Обработка ошибки, если не удалось соединиться с сервером API Директа
	except ConnectionError:
		# В данном случае мы рекомендуем повторить запрос позднее
		print("Произошла ошибка соединения с сервером API.")
		# Принудительный выход из цикла
		break

	# Если возникла какая-либо другая ошибка
	except:
		# В данном случае мы рекомендуем проанализировать действия приложения
		print("Произошла непредвиденная ошибка.")
		# Принудительный выход из цикла
		break
