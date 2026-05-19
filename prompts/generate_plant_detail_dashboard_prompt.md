# Prompt: Generate Plant Detail Dashboard

## Задача
Побудувати plant-detail.html — аналітичний профіль одного заводу.

## Вхідні дані
- `/data/processed/plant_details/[plant_id].json`
- URL параметр: `?id=[plant_id]`
- Дизайн-бриф від UI/UX Agent

## Секції сторінки

### 1. Plant Header
- Назва, місто, власник, статус, стратегічна важливість
- Короткий summary (2-3 речення)

### 2. Production Route Diagram (SVG)
- Візуальна схема: BF → BOF → Casting → Rolling → Products
- або: EAF → Casting → Rolling → Products

### 3. Aggregates Section
- Таблиця агрегатів
- Поля: назва, тип, статус, потужність, вихід, тренд

### 4. Products Section
- Картки продуктів (rebar, wire rod, billets тощо)
- Поля: потужність, виробництво, продажі, тренд vs 2024

### 5. Performance 2025
- KPI картки: виробництво, продажі, експорт, утилізація, виручка
- Тренд vs 2024

### 6. Market Context
- Чеський ринок сталі, позиція заводу

### 7. News & Activity
- Хронологія подій 2024-2025
- Колір по типу: інвестиції (зелений), ризики (помаранчевий), негатив (червоний)

### 8. Sources
- Список джерел з посиланнями

## Технічні вимоги
- Vanilla JS
- Дані з JSON через URL параметр
- Кнопка "← Back to Map"
- Responsive layout
