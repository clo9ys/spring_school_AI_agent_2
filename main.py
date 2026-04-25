from smolagents import ToolCallingAgent, LiteLLMModel
from tools.market_tools import MarketAnalyzerTool, CarDiscoveryTool
from tools.wiki_tool import CarWikiTool


def main():
    model = LiteLLMModel(
        model_id="ollama/qwen2.5-coder:7b",
        api_base="http://localhost:11434"
    )

    tools = [CarWikiTool(), MarketAnalyzerTool(), CarDiscoveryTool()]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        add_base_tools=False,
        max_steps=5
    )

    print("\n" + "=" * 50)
    print("🚗 CAR SCOUT AI: ТВОЙ АВТО-ЭКСПЕРТ (macOS Edition)")
    print("Я помогу тебе найти лучший автомобиль по бюджету.")
    print("=" * 50 + "\n")

    MASTER_PROMPT = """Ты — ведущий авто-эксперт и твой совет на вес золота. 
    ТВОЯ ЗАДАЧА — СОСТАВИТЬ ПОДРОБНЫЙ ОТЧЕТ И ДАТЬ КОНКРЕТНЫЙ СОВЕТ. 
    
    ПОШАГОВЫЙ ПЛАН:
    1. Сначала собери данные через инструменты ('get_car_history_and_specs', 'analyze_market_stats' или 'discover_cars').
    2. В ФИНАЛЬНОМ ОТВЕТЕ СТРОГО СОБЛЮДАЙ СТРУКТУРУ:
    
    **ОБЗОР ВАРИАНТОВ**
    (Для каждой машины: Марка, Цена, Надежность и кратко Минусы. С ПЕРЕНОСОМ СТРОК!)
    
    **ВЕРДИКТ ЭКСПЕРТА**
    (Здесь твой живой совет. Сравни найденные машины. 
    Выдели одного фаворита, который лучше всего подходит под запрос пользователя. 
    Напиши: "Мой выбор — [Модель], потому что...". 
    Дай рекомендацию: стоит ли брать сейчас или поискать что-то другое.)
    
    ВАЖНО: Пиши человечно, как опытный подборщик. Избегай сухих списков без выводов.
    ---
    Запрос пользователя: """

    while True:
        try:
            user_query = input("👤 Вы: ").strip()
            if not user_query or user_query.lower() in ["выход", "exit"]: break

            full_query = MASTER_PROMPT + user_query
            agent.run(full_query)
            print("-" * 30)

        except KeyboardInterrupt:
            print("\n👋 До встречи!")
            break
        except Exception as e:
            print(f"🤖 Ошибка: {e}")


if __name__ == "__main__":
    main()