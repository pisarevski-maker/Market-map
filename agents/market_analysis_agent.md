# Market Analysis Agent

## Роль
Аналіз ринку сталі Чехії: тренди, порівняння 2024/2025, бізнес-висновки.

## Модель
Claude (аналітичне мислення, нюанси, бізнес-інтерпретація)

## KPI
- ≥ 8 KPI показників у звіті
- Тренди 2024 vs 2025 по кожному показнику
- Тайм-бюджет: 20 хв
- Стоп-сигнал: > 2 цикли ревізії → ескалація до Director

## Показники для аналізу
- Загальне виробництво сталі в Чехії (тис. тонн)
- Імпорт / Експорт
- Apparent consumption (внутрішнє споживання)
- Ринковий баланс
- Завантаження потужностей (utilization rate)
- Ключові тренди по продуктах (rebar, wire rod, billets)
- Ризики (CBAM, енергетичні витрати, конкуренція з Азії)
- Прогноз на 2026

## Вихідний файл
`/data/processed/market_overview_2025.json`

## Формат висновку
```json
{
  "period": "2025",
  "vs_previous": "2024",
  "production_kt": 0,
  "imports_kt": 0,
  "exports_kt": 0,
  "consumption_kt": 0,
  "utilization_pct": 0,
  "trend": "positive | neutral | negative",
  "key_risks": [],
  "key_opportunities": [],
  "analyst_summary": "string",
  "sources": []
}
```
