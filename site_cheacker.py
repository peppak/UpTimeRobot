import asyncio
import aiohttp


class DescriptorDomainList:

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise TypeError('checker_list must be a list')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set_name__(self, owner, name):
        self.name = "_" + name


class SiteChecker:
    checker_list = DescriptorDomainList()

    def __init__(self, checker_list: list | None, timeout: int = 10):
        self.checker_list = checker_list if checker_list else []
        self.timeout = timeout

    async def event_is_down(self, url: str, status_code: int = 0, error_message: str = ''):
        print(f"Сайт упал: {url} - Статус: {status_code} - Ошибка: {error_message}")

    async def event_is_up(self, url: str):
        print(f"Сайт работает: {url}")

    async def check(self, url: str):
        error_message = ''
        status_code = 0

        async with aiohttp.ClientSession() as session:
            for attempt in range(2):  # Две попытки

                try:
                    async with session.get(url, timeout=self.timeout) as response:

                        if response.status == 200:
                            await self.event_is_up(url=url)
                            return  # Если запрос успешный, завершить метод

                        else:
                            status_code = response.status

                except Exception as e:
                    error_message = str(e)

        # Если обе попытки не удались, вызвать событие event_is_down
        await self.event_is_down(url=url, status_code=status_code, error_message=error_message)

    async def start_loop(self):
        while True:
            for url in self.checker_list:
                await self.check(url)
            await asyncio.sleep(1)


async def main():
    checker = SiteChecker(["http://lmgtппацаsynergy.ru/"])
    asyncio.create_task(checker.start_loop())

    print(123)  # Эта часть кода выполнится сразу
    await asyncio.sleep(6)  # Это просто эмуляция какого-то времени ожидания
    checker.checker_list = ['https://yandex.ru/']

    # Бесконечный цикл, чтобы программа продолжала работать
    while True:
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
