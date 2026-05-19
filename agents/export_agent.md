# Export Agent

## Роль
Упаковка фінального продукту для запуску в один клік.

## Модель
llama3.2:3b (рутина, шаблонні файли)

## Задачі
1. Зібрати всі файли dashboard/ і data/ у /output/
2. Створити ZIP архів
3. Створити Dockerfile для запуску через браузер
4. Створити docker-compose.yml
5. Перевірити що все запускається

## Вихідні файли
```
/output/
├── czech-steel-dashboard/     ← весь проект
├── czech-steel-dashboard.zip  ← архів для пересилки
├── Dockerfile
├── docker-compose.yml
└── START.md                   ← інструкція запуску
```

## Dockerfile (шаблон)
```dockerfile
FROM nginx:alpine
COPY dashboard/ /usr/share/nginx/html/
COPY data/ /usr/share/nginx/html/data/
EXPOSE 80
```

## docker-compose.yml (шаблон)
```yaml
version: '3'
services:
  czech-steel-dashboard:
    build: .
    ports:
      - "8080:80"
```

## START.md інструкція
- Варіант 1: відкрити index.html напряму у браузері
- Варіант 2: docker-compose up → http://localhost:8080
