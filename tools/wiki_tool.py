import requests
from smolagents import Tool
from tools.utils import handle_tool_errors


class CarWikiTool(Tool):
    name = "get_car_history_and_specs"
    description = "Получает краткое техническое описание и историю модели автомобиля из Википедии."
    inputs = {
        "model_name": {"type": "string", "description": "Название модели автомобиля (например, BMW M5)"}
    }
    output_type = "string"

    @handle_tool_errors
    def forward(self, model_name: str) -> str:
        search_url = "https://ru.wikipedia.org/w/api.php"

        headers = {
            "User-Agent": "CarScoutAgent/1.0 (email@example.com)"
        }

        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": model_name,
            "utf8": 1,
            "srlimit": 1
        }

        response = requests.get(search_url, params=search_params, headers=headers)
        if response.status_code != 200:
            return f"Ошибка Википедии: сервер вернул код {response.status_code}"

        search_res = response.json()

        if not search_res.get("query", {}).get("search"):
            return f"К сожалению, в Википедии нет точного совпадения для '{model_name}'. Попробуйте сократить запрос"

        page_title = search_res["query"]["search"][0]["title"]

        content_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "titles": page_title,
            "exintro": True,
            "explaintext": True,
            "utf8": 1
        }

        content_res = requests.get(search_url, params=content_params, headers=headers).json()
        pages = content_res.get("query", {}).get("pages", {})
        page_id = list(pages.keys())[0]

        if page_id == "-1":
            return f"Страница '{page_title}' не найдена."

        extract = pages[page_id].get("extract", "")

        return f"Справка из энциклопедии ({page_title}):\n{extract[:600]}..."