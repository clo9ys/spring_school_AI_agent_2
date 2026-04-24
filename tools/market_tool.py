import os
from typing import List, Dict, Optional
from pathlib import Path
import json
from smolagents import Tool
from tools.utils import handle_tool_errors


class MarketAnalyzerTool(Tool):
    name = "analyze_market_stats"
    description = "Предоставляет рыночные данные (цена, надежность) из локальной базы данных."
    inputs = {
        "model_name": {"type": "string", "description": "Название модели автомобиля"}
    }
    output_type = "string"

    @handle_tool_errors
    def forward(self, model_name: str) -> str:
        data_path = os.path.join("data", "market_db.json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            if item["model"].lower() in model_name.lower():
                return (f"Статистика по {model_name}: Средняя цена {item['avg_price']} руб. "
                        f"Индекс надежности: {item['reliability_index']}/10. Плюсы: {item['pros']}. Минусы: {item['cons']}")

        return f"Модель '{model_name}' не найдена в локальной базе."


class CarDiscoveryTool(Tool):
    name = "discover_cars"
    description = "Ищет автомобили в базе данных по бюджету и году выпуска."
    inputs = {
        "max_price": {"type": "integer", "description": "Максимальный бюджет в рублях", "nullable": True},
        "min_year": {"type": "integer", "description": "Минимальный год выпуска", "nullable": True}
    }
    output_type = "string"

    @handle_tool_errors
    def forward(self, max_price: Optional[int] = None, min_year: Optional[int] = None) -> str:
        base_path = Path(__file__).parent.parent
        data_path = base_path / "data" / "cars_data.json"

        with open(data_path, "r", encoding="utf-8") as f:
            data: List[Dict] = json.load(f)

        results = []
        for car in data:
            # Проверяем бюджет (если указан)
            price_ok = (max_price is None) or (car["avg_price"] <= max_price)
            # Проверяем год (если указан) - для этого в JSON нужно добавить поле 'year' или 'start_year'
            year_ok = (min_year is None) or (car.get("year_produced", 0) >= min_year)

            if price_ok and year_ok:
                results.append(f"{car['brand']} {car['model']} ({car['avg_price']:,} руб.)")

        if not results:
            return "К сожалению, под ваш бюджет и критерии ничего не найдено."

        return "Подходящие варианты:\n" + "\n".join(results[:5])