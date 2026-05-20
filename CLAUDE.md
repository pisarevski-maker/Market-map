# CLAUDE.md — Правила проекту Czech Steel Dashboard

## Правила даних
- Ніколи не вигадувати точні цифри
- Якщо дані недоступні → писати "To be verified"
- Чітко розрізняти: факт / оцінка / аналітична інтерпретація
- Позначати estimates відповідним тегом у JSON: `"source_type": "estimated"`

## Правила дизайну
- Білий фон (#FFFFFF), темна типографіка (#1E1E1E)
- Бургундські акценти: #7A1F2B / #9B1C31 / #C94555
- Багато white space — уникати візуального перевантаження
- Елегантна типографіка, тонкі роздільники, м'які тіні
- Дашборд має виглядати як board presentation / executive report
- Надавати перевагу SVG над растровою графікою

## UX правила
- Дашборд має відчуватись: швидко, чисто, сучасно, аналітично, преміально
- Адаптивний layout (responsive)
- Hover interactions на маркерах карти
- Кліки на завод → відкривають plant-detail.html

## Правила агентів
- Director дає "зелене світло" перед кожним переходом між фазами
- Кожен агент отримує чіткий бриф перед стартом
- Claude приймає всі рішення що потребують судження

## Git commits — ОБОВ'ЯЗКОВО (Claude робить без запитань)
Claude як куратор проекту зобов'язаний робити git commit після кожної завершеної фази:

| Тригер | Команда коміту |
|---|---|
| Структура папок + конфіги створені | `git commit -m "init: project structure + agent configs"` |
| Research Agent завершив збір даних | `git commit -m "research: {country} steel plants data collected"` |
| JSON файли заводів згенеровані | `git commit -m "data: plant JSON files generated and validated"` |
| index.html готовий | `git commit -m "dashboard: map dashboard index.html"` |
| plant-detail.html готовий | `git commit -m "dashboard: plant detail page"` |
| Ринкові дані інтегровані | `git commit -m "feat: market panel + market_context.json"` |
| QA пройдений | `git commit -m "qa: all checks passed, ready for export"` |
| Будь-яке важливе виправлення | `git commit -m "fix: {опис}"` |

**Правило:** Не чекати кінця проекту. Коміт = страховка. Кожна фаза = окрема стабільна точка в git history.

**Якщо git показує "nothing to commit" на Windows/OneDrive:** виконати `del .git\index && git add -A` перед комітом (G-16).

## Тренди кольорів
- Зростання / інвестиції → #2E7D32 (зелений)
- Невизначеність / ризики → #E6862C (помаранчевий)
- Спад / банкрутство → #B3261E (червоний)
