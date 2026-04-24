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
        base_path = Path(__file__).parent.parent
        data_path = base_path / "data" / "cars_data.json"

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        target = model_name.lower()
        result = next(
            (item for item in data if target in item["model"].lower() or item["model"].lower() in target),
            None
        )

        if result:
            # Используем .get() с дефолтными значениями, чтобы не было KeyError
            price = result.get('avg_price', 'Нет данных')
            # Проверяем оба варианта ключа на всякий случай
            rel = result.get('reliability_score') or 'Нет данных'
            pros = result.get('pros', 'Не указаны')
            cons = result.get('cons', 'Не указаны')

            return (
                f"Результаты анализа рынка для {result.get('brand')} {result.get('model')}:\n"
                f"- Средняя цена: {price} руб.\n"
                f"- Индекс надежности: {rel}/10\n"
                f"- Плюсы: {pros}\n"
                f"- Минусы: {cons}"
            )

        return f"Модель '{model_name}' отсутствует в локальном датасете."


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