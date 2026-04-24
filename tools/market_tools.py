from typing import Optional
from pathlib import Path
import json
from smolagents import Tool
from tools.utils import handle_tool_errors


class MarketAnalyzerTool(Tool):
    name = "analyze_market_stats"
    description = "Получает подробную информацию (надежность, плюсы/минусы) по конкретной МОДЕЛИ (например, 'BMW 3 Series' или 'Camry')."
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
        result = None

        for item in data:
            db_model = item["model"].lower()
            if db_model in target or target in db_model:
                result = item
                break

        if result:
            return (
                f"РЫНОЧНЫЕ ДАННЫЕ ({result['brand']} {result['model']}):\n"
                f"- Цена: {result['avg_price']:,} руб.\n"
                f"- Надежность: {result['reliability_score']}/10\n"
                f"- Особенности: {result.get('common_issues', 'Нет данных')}"
            )
        return f"Модель '{model_name}' не найдена в ценовой базе. Используй только данные из Википедии."


class CarDiscoveryTool(Tool):
    name = "discover_cars"
    description = "Ищет машины только по БЮДЖЕТУ и ГОДУ. Не использовать для поиска конкретных моделей по названию."
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
            data = json.load(f)

        filtered = [car for car in data if
                    (max_price is None or car["avg_price"] <= max_price) and
                    (min_year is None or car.get("year_produced", 0) >= min_year)]

        if not filtered:
            return "К сожалению, ничего не найдено."

        if max_price and max_price > 1000000:
            min_threshold = max_price * 0.8
            premium_candidates = [car for car in filtered if car["avg_price"] >= min_threshold]

            if len(premium_candidates) >= 3:
                filtered = premium_candidates

        filtered.sort(key=lambda x: x.get('reliability_score', 0), reverse=True)
        final_selection = filtered[:3]

        output = f"🏁 Лучшие варианты в сегменте до {max_price:,} руб.:\n\n"
        for i, car in enumerate(final_selection, 1):
            score = car.get('reliability_score', 'N/A')
            issues = car.get('common_issues', 'Нет данных')
            output += (f"{i}. **{car['brand']} {car['model']}**\n"
                       f"   💰 Цена: {car['avg_price']:,} руб.\n"
                       f"   🛡️ Надежность: {score}/10\n"
                       f"   ⚠️ Особенности: {issues}\n\n")
        return output
