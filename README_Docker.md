# Docker Setup для Ebenevo Bot

## Быстрый старт

### 1. Сборка и запуск с Docker Compose
```bash
docker-compose up --build
```

### 2. Запуск в фоновом режиме
```bash
docker-compose up -d --build
```

### 3. Остановка
```bash
docker-compose down
```

## Структура проекта

```
ebenevo-bot/
├── Dockerfile              # Конфигурация Docker образа
├── docker-compose.yml      # Конфигурация Docker Compose
├── requirements.txt        # Python зависимости
├── .dockerignore          # Исключения для Docker
├── .env                   # Переменные окружения
├── main.py               # Главный файл бота
├── core/                 # Основные модули
├── modules/              # Модули бота
├── data/                 # База данных (монтируется в контейнер)
└── images/               # Изображения для бота
```

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_bot_token_here
CHANNEL_ID=your_admin_channel_id_here
```

## Особенности Docker конфигурации

### Dockerfile
- Использует Python 3.10
- Устанавливает зависимости из `requirements.txt`
- Создает папку `/app/data` для базы данных
- Копирует все файлы проекта в контейнер

### docker-compose.yml
- Монтирует папку `./data` в контейнер для сохранения базы данных
- Монтирует файл `.env` для переменных окружения
- Настроен автоперезапуск при сбоях
- Включен буферизованный вывод для логов

## Зависимости

Все зависимости указаны в `requirements.txt`:
- `pyTelegramBotAPI==4.24.0` - Telegram Bot API
- `python-dotenv==1.1.1` - Загрузка переменных окружения
- `tinydb==4.8.2` - База данных
- `requests==2.32.3` - HTTP запросы
- `beautifulsoup4==4.14.2` - Парсинг HTML

## Логи и отладка

### Просмотр логов
```bash
docker-compose logs -f ebenevo-bot
```

### Вход в контейнер
```bash
docker-compose exec ebenevo-bot bash
```

### Перезапуск бота
```bash
docker-compose restart ebenevo-bot
```

## Обновление

1. Остановите контейнер:
   ```bash
   docker-compose down
   ```

2. Пересоберите образ:
   ```bash
   docker-compose up --build
   ```

## Резервное копирование

База данных сохраняется в папке `./data/` на хосте. Для резервного копирования просто скопируйте эту папку.

## Устранение проблем

### Проблема: Контейнер не запускается
- Проверьте файл `.env` и наличие токена бота
- Убедитесь, что порты не заняты
- Проверьте логи: `docker-compose logs ebenevo-bot`

### Проблема: Ошибки импорта
- Убедитесь, что все файлы скопированы в контейнер
- Проверьте `requirements.txt`
- Пересоберите образ: `docker-compose up --build`
