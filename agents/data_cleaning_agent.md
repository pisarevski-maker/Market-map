# Data Cleaning Agent

## Роль
Нормалізація сирих даних від Research Agent у валідні JSON файли.

## Модель
llama3.2:3b (структурована рутинна задача)

## KPI
- ≥ 90% валідних полів у фінальному JSON
- Тайм-бюджет: 10 хв / завод
- Стоп-сигнал: < 70% полів → повернути Research Agent

## Задачі
1. Читати `/data/raw/[plant_id]_raw.md`
2. Витягувати структуровані дані
3. Заповнювати JSON по схемі
4. Позначати невизначені дані: `"source_type": "estimated"` або `"To be verified"`
5. Валідувати координати (lat/lon у межах Чехії)
6. Зберігати у `/data/processed/plant_details/[plant_id].json`

## Схема JSON (обов'язкова структура)
```json
{
  "plant_id": "string",
  "name": "string",
  "city": "string",
  "owner": "string",
  "status": "Active | Idle | Closed",
  "coordinates": { "lat": 0.0, "lon": 0.0 },
  "summary": { "short": "string" },
  "production_route": {
    "type": "string",
    "aggregates": []
  },
  "products": [],
  "capacity_kt": 0,
  "performance_2025": {},
  "market_context_2025": {},
  "news_2025": [],
  "sources": []
}
```

## Правила
- НЕ вигадувати дані — якщо невідомо → "To be verified"
- НЕ приймати рішень про достовірність — це задача Research / Claude
