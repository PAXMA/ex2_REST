import sys
import requests
from requests import exceptions

class Nalog:
    def __init__(self):
        pass

    def get_payment_details(self, ifns, oktmo):
        url = "https://service.nalog.ru/addrno-proc.json"
        data = {"c": "next",
                "step": 1,
                "npKind":"fl",
                "objectAddr":None,
                "objectAddr_zip":None,
                "objectAddr_ifns":None,
                "objectAddr_okatom":None,
                "ifns": ifns,
                "oktmmf": oktmo,
                "PreventChromeAutocomplete":None
                }
        try:
            response = requests.post(url, data=data)
        except:
            print(f"Не удалось отравить запрос серверу.")
            return
        if response.status_code != 200:
            print(f"Не удалось выполнить запрос с заданными аргументами. Код ответа: {response.status_code}.\n"
                  f"Пояснение от сервера: {response.text}.")
            return
        try:
            resp_data = response.json()
        except exceptions.JSONDecodeError:
            print(f"Что-то пошло не так при декодировании ответа от сервера.")
            return
        ret = []
        ret.append(resp_data["payeeDetails"]["payeeName"])
        ret.append(resp_data["payeeDetails"]["payeeInn"])
        ret.append(resp_data["payeeDetails"]["payeeKpp"])
        ret.append(resp_data["payeeDetails"]["bankName"])
        ret.append(resp_data["payeeDetails"]["bankBic"])
        ret.append(resp_data["payeeDetails"]["payeeAcc"])
        return ret

if __name__ == '__main__':
    a = Nalog()

    try:
        res = a.get_payment_details(*sys.argv[1:])
        if res:
            print(res)
    except:
        print(f"Ошибка в кол-ве аргументов. Для работы программы необходимо указать 2 аргумента: Код ИФНС и ОКТМО."
              f"Например, так: python main.py 7840 40913000")
