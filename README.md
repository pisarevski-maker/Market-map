# Czech Steel Dashboard

Інтерактивний HTML-дашборд розвідки ринку сталі Чехії.

## Швидкий старт

### Варіант 1 — напряму у браузері
```
Відкрити: dashboard/index.html
```

### Варіант 2 — Docker
```bash
docker-compose up
# Відкрити: http://localhost:8080
```

## Структура
```
agents/      ← конфіги агентів
data/        ← сирі та оброблені дані
dashboard/   ← HTML/CSS/JS продукт
prompts/     ← промпти для агентів
output/      ← фінальний пакет для пересилки
```

## Агенти
| Агент | Модель | Роль |
|---|---|---|
| Director | Claude | Координація |
| Research | Claude | Збір даних |
| Data Cleaning | llama3.2:3b | JSON нормалізація |
| Market Analysis | Claude | Аналітика |
| UI/UX | Claude | Дизайн-брифи |
| Dashboard Builder | phi3:mini + Claude | HTML/CSS/SVG |
| QA + Bug Fixer | gemma3:4b + Claude | Верифікація |
| Export | llama3.2:3b | Упаковка |

## Статус
Дивись: `todo.md`

## Архітектура
Дивись: `../ARCHITECTURE.md`
