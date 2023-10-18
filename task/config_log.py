from loguru import logger


class LogRules:
    def do_logs(self, response):
        logger.add("./task/debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 KB")
        if response.status_code == 200:
            status_message = "Успех"
            logger.info(f"{status_message}:Status Code ({response.status_code}, {response.reason})")
        else:
            status_message = "Неуспех"
            logger.error(f"{status_message}: Status Code ({response.status_code}, {response.reason}), Message: {response.text}")

    async def do_logs_async(self, response):
        if response.status == 200:
            status_message = "Успех"
            logger.info(f"{status_message}:Status Code ({response.status}, {response.reason})")
        else:
            status_message = "Неуспех"
            logger.error(f"{status_message}:Status Code ({response.status}, {response.reason}), Message: {await response.text()}")


to_log = LogRules()
