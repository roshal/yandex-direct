# -*- coding: utf-8 -*-
import requests, json

# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys

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

# --- Входные данные ---
# Адрес сервиса Ads для отправки JSON-запросов (регистрозависимый)
CampaignsURL = "https://api.direct.yandex.com/json/v5/ads"
OAuth-токен пользователя, от имени которого будут выполняться запросы
token = "ТОКЕН"

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = "ЛОГИН_КЛИЕНТА"

# Идентификатор группы объявлений, в которую будет добавлено новое объявление
adGroupId = 1234567

# --- Подготовка, выполнение и обработка запроса ---
# Создание HTTP-заголовков запроса
headers = {
	"Authorization": "Bearer " + token,  # OAuth-токен. Использование слова Bearer обязательно
	"Client-Login": clientLogin,  # Логин клиента рекламного агентства
	"Accept-Language": "ru",  # Язык ответных сообщений.
}

# Создание тела запроса
body = {
	"method": "add",                                    # Используемый метод
	"params": {
		"Ads": [{
			"AdGroupId": adGroupId,
			"TextAd": {                                 # Параметры объявления
				"Title": u"Заголовок объявления",
				"Text": u"Текст объявления",
				"Mobile": "NO",
				"Href": "http://www.yandex.ru"
			}
		}
		]
	}
}

# Кодирование тела запроса в JSON
jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

# Выполнение запроса
try:
	result = requests.post(CampaignsURL, jsonBody, headers=headers)

	# Отладочная инфомрация
	# print("Заголовки запроса: {}".format(result.request.headers))
	# print("Запрос: {}".format(u(result.request.body)))
	# print("Заголовки ответа: {}".format(result.headers))
	# print("Ответ: {}".format(u(result.text)))
	# print("\n")

	# Обработка запроса
	if result.status_code != 200 or result.json().get("error", False):
		print("Произошла ошибка при обращении к серверу API Директа.")
		print("Код ошибки: {}".format(result.json()["error"]["error_code"]))
		print("Описание ошибки: {}".format(u(result.json()["error"]["error_detail"])))
		print("RequestId запроса: {}".format(result.headers.get("RequestId", False)))
	else:
		# Вывод результата
		print("RequestId запроса: {}".format(result.headers.get("RequestId", False)))
		print("Информация о баллах: {}".format(result.headers.get("Units", False)))
		# Обработка всех элементов массива AddResults, где каждый элемент соотвествует одному объявлению
		for add in result.json()["result"]["AddResults"]:
			# Обработка вложенных элементов (может быть либо Errors, либо Id и, возможно, Warnings)
			if add.get("Errors", False):
				# Если присутствует массив Errors, то объявление не создано из-за ошибки (ошибок может быть несколько)
				for error in add["Errors"]:
					print("Ошибка: {} - {} ({})".format(error["Code"], u(error["Message"]),
												 u(error["Details"])))
			else:
				# Если присутствует параметр Id, то объявление создано
				print("Создано объявление №{}".format(add["Id"]))
				# Если присутствует массив Warnings, то объявление создано, но есть предупреждения (предупреждений может быть несколько)
				if add.get("Warnings", False):
					for warning in add["Warnings"]:
						print("Предупреждение: {} - {} ({})".format(warning["Code"], u(warning["Message"]),
														 u(warning["Details"])))

# Обработка ошибки, если не удалось соединиться с сервером API Директа
except ConnectionError:
	# В данном случае мы рекомендуем повторить запрос позднее
	print("Произошла ошибка соединения с сервером API.")

# Если возникла какая-либо другая ошибка
except:
	# В данном случае мы рекомендуем проанализировать действия приложения
	print("Произошла непредвиденная ошибка.")
