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

    MASTER_PROMPT = """Ты — ведущий авто-эксперт. 
        ТВОЯ ЗАДАЧА — СОСТАВИТЬ ПОДРОБНЫЙ ОТЧЕТ. 

        ПОШАГОВЫЙ ПЛАН:
        1. ОБЯЗАТЕЛЬНО начни с 'get_car_history_and_specs'. 
        2. Затем используй 'analyze_market_stats'.

        ПРАВИЛА ОФОРМЛЕНИЯ ФИНАЛЬНОГО ОТВЕТА:
        - ЗАПРЕЩЕНО давать пустые ответы или только заголовки.
        - ТЫ ОБЯЗАН СКОПИРОВАТЬ И ПЕРЕСКАЗАТЬ информацию из Википедии (минимум 3-4 предложения).
        - ТЫ ОБЯЗАН ВЫВЕСТИ все цифры из локальной базы (Цена, Надежность, ТТХ).
        - Используй структуру:

          📚 **ТЕХНИЧЕСКАЯ ИСТОРИЯ**
          (Текст из Википедии здесь)

          💰 **РЫНОЧНАЯ АНАЛИТИКА**
          (Цена, надежность и проблемы здесь)

          🛠 **ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ**
          (Двигатель, л.с., вес здесь)

        Пиши СРАЗУ ПОЛНЫЙ ТЕКСТ на русском языке.
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