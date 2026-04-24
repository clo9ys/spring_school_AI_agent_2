import requests
from smolagents import Tool

class VehicleInfoTool(Tool):
    name = "get_vehicle_specs"
    description = "Получает технические характеристики марки авто через внешнее API."
    inputs = {
        "brand": {"type": "string", "description": "Марка авто на английском (например, Honda)"}
    }
    output_type = "string"

    def forward(self, brand: str) -> str:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{brand}?format=json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                models = [item['Model_Name'] for item in response.json()['Results'][:5]]
                return f"Популярные модели {brand} в глобальном реестре: {', '.join(models)}"
            return f"Не удалось получить данные для бренда {brand}"
        except Exception as e:
            return f"Ошибка API: {str(e)}"