# Prompt: Generate Map Dashboard

## Задача
Побудувати index.html — інтерактивна карта чеських виробників сталі.

## Вхідні дані
- `/data/processed/czech_steel_plants.json`
- `/data/geo/czechia.geojson` (або вбудований SVG)
- `/dashboard/config/colors.js`
- `/dashboard/config/layout.js`
- `/dashboard/config/map_settings.js`
- Дизайн-бриф від UI/UX Agent

## Технічні вимоги
- Vanilla JS (без фреймворків)
- SVG карта Чехії вбудована у HTML
- Дані завантажуються з JSON через fetch()
- Без зовнішніх залежностей (все inline або локально)
- Responsive layout

## UX Flow
1. Сторінка завантажується → відображається карта
2. Hover на маркер → показує tooltip з назвою заводу
3. Клік на маркер → відкриває plant-detail.html?id=[plant_id]
4. Фільтри зліва → фільтрують маркери на карті
5. Market overview widgets → 4 KPI картки зверху або збоку

## Компоненти
- Header (назва проекту, підзаголовок)
- Czechia SVG Map з маркерами
- Sidebar / Tooltip
- Market Overview KPI cards
- Filter panel
- Footer з джерелами

## Дизайн
Дивись ARCHITECTURE.md розділ "Дизайн-система".
Bloomberg / McKinsey стиль. Білий фон, бургундські акценти.
