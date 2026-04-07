# Frontend — CLAUDE.md

Vue 3 SPA для регистрации курьеров (Bolt, Foodora). Чистый JavaScript (не TypeScript).

## Стек

- **Vue 3** + `<script setup>` (Composition API)
- **Vite** — сборщик
- **Pinia** — state management
- **Vue Router 5** — `createWebHistory()`, чистые URL
- **vue-i18n 11** — мультиязычность (en, ru, cz)
- **Axios** — HTTP-клиент
- **@vueuse/core** — `useMediaQuery` для определения мобильного

## Структура

```
src/
├── api/
│   ├── api.js          # Axios instance (baseURL из VITE_API_URL, timeout 10s)
│   └── posts.js        # createPost(), createFile() — все запросы к бэкенду
├── assets/
│   ├── base.css        # CSS-переменные, шрифты
│   └── main.css        # Глобальные утилитарные классы
├── components/
│   ├── *Comp.vue       # Компоненты десктопа
│   └── mobile/
│       └── m*Comp.vue  # Мобильные варианты (префикс m)
├── i18n/
│   ├── index.js
│   ├── en.json / ru.json / cz.json
├── router/index.js
├── stores/
│   ├── uiStore.js      # isMobile (breakpoint 768px)
│   └── localeStore.js  # locale → localStorage
└── views/              # Компоненты-страницы (роуты)
```

## Роуты

| Путь | Компонент | Описание |
|------|-----------|----------|
| `/` | homeView | Лендинг |
| `/select-platform` | selectPlatformView | Выбор платформы |
| `/form/:company` | formView | Форма регистрации |
| `/success/:company` | successSendFormView | Успешная отправка |

`:company` — `bolt` или `foodora`, влияет на логотип и цвета.

## API

- `VITE_API_URL=http://127.0.0.1:8000/api/v1` (из `.env`)
- `POST /users` — регистрация пользователя
- `POST /files` — загрузка документов (multipart/form-data)
- `POST /documents` — привязка файлов к пользователю

Поток при отправке формы: создать пользователя → загрузить файлы → привязать документы → редирект на `/success/:company`.

## Соглашения

**Именование компонентов:** camelCase с суффиксом `Comp` (например, `headerComp.vue`).

**Мобильные компоненты:** отдельные `.vue`-файлы с префиксом `m` в папке `mobile/`. Подключаются условно через `uiStore.isMobile`.

**Импорты:** алиас `@/` → `src/`.

**CSS:** scoped-стили в компонентах + глобальные классы в `main.css`. Переменные бренда:
- `--brand-color: #C02A22` (красный)
- `--bolt-color: #34D086` (зелёный)
- `--foodora-color: #DF1068` (розовый)

**Локализация:** весь UI-текст через `$t()` / `useI18n()`. Ключи — в JSON-файлах в `i18n/`.

**Форма:** `reactive()` для данных, `computed()` для валидации, `watch()` для побочных эффектов (например, сброс файлов при смене гражданства). Чехи и не-чехи получают разный набор документов для загрузки.

## Команды

```bash
pnpm dev       # dev-сервер
pnpm build     # production-сборка
pnpm preview   # превью сборки
```

## Примечания

- Тестов нет.
- TypeScript не используется — только JS.
- Шрифты: Montserrat, Mulish, Actor (Google Fonts).
