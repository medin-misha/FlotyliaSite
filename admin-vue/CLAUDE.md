# admin-vue

Административная панель для управления данными сайта. Vue 3 SPA с Vue Router — маршрутизатор управляет URL и guard-ами, Pinia хранит UI-состояние (какой раздел открыт, table/create/detail).

## Стек

- **Vue 3** + Vite 7, JavaScript (не TypeScript)
- **Vue Router 4** — URL-навигация, auth guard, синхронизация query-параметров
- **Pinia** — стейт-менеджмент (pageStore, statesStore, authStore, requestStates)
- **Axios** — HTTP-клиент
- **pnpm** — пакетный менеджер
- **Nginx** — раздача статики в Docker

## Команды

```bash
pnpm dev        # dev-сервер с HMR
pnpm build      # production-сборка
pnpm preview    # предпросмотр сборки
pnpm lint       # oxlint + eslint с автофиксом
pnpm format     # prettier по src/
```

## Переменные окружения (.env)

```
VITE_API_URL=http://127.0.0.1:8000/api/v1
VITE_HTTPS_ONLY=false
```

При сборке Docker передаются как build args.

## Архитектура

### Гибридная навигация: Router + Pinia

Vue Router обрабатывает URL и auth-guard, но рендеринг делегирован Pinia-стейту через `afterEach`:

- **`beforeEach`** — редирект на `/login` если не авторизован, и обратно если авторизован
- **`afterEach`** — синхронизирует URL → Pinia: путь и query (`search`, `page`, `filter`) записываются в `pageStore` и `statesStore`

Все маршруты используют `PlaceholderComponent` (пустой `<div>`), реальный рендеринг — через `App.vue` + `bodyComp.vue` на основе состояния Pinia.

Маршруты: `/login`, `/users`, `/users/create`, `/users/:id`, `/admins`, `/admins/create`, `/admins/:id`. Всё остальное → redirect на `/users`.

### Управление UI-состоянием

- `pageStore.setPage(endpoint, name, createSchema, schema)` — переключить раздел
- `statesStore` — текущее представление: `table` | `create` | `detail`

Клик по пункту меню → `router.push('/users')`, `afterEach` → `pageStore.setPage(...)` + `statesStore.setTableState()`.

### Schema-driven UI

Каждый раздел описывается двумя схемами в `src/forms/`:
- `schema` — поля для отображения/редактирования
- `createSchema` — поля для формы создания

Схема поля:
```js
{ key: 'name', label: 'Имя', component: markRaw(StringComp), readonly: false }
// для select:
{ key: 'status', label: 'Статус', component: markRaw(SelectComp), options: ['active', 'inactive'] }
// для файлов:
{ key: 'contract_file', label: 'Файл', component: markRaw(FileComp), isFile: true }
```

Компоненты полей используют `defineModel('value')` для v-model-биндинга.

### Разделы (src/forms/)

| Файл | Endpoint | Описание |
|------|----------|----------|
| `userFrom.js` | `/users` | Пользователи с документами |
| `adminForm.js` | `/admin` | Администраторы |
| `contractForm.js` | `/contracts` | Договоры |
| `transportForm.js` | `/transports` | Транспорт |
| `productForm.js` | `/product` | Продукты/страховые случаи |

## Структура src/

```
src/
├── api/
│   ├── api.js           # axios-инстанс с interceptors (401 → logout)
│   ├── auth.js          # login, createAdmin, getAdmins, deleteAdmin
│   ├── getters.js       # getUniversal, getDetail, getExport (xlsx)
│   └── posts.js         # createPost, updatePost, deletePost, createFile
├── router/
│   └── index.js         # маршруты, beforeEach (auth guard), afterEach (URL → Pinia sync)
├── stores/
│   ├── auth.js          # user/token в cookies (7 дней, sameSite strict)
│   ├── page.js          # текущий раздел + пагинация/поиск/фильтр
│   ├── states.js        # table/create/detail + instance_id
│   └── requestStates.js # waiting/networkError/emptyList
├── forms/               # схемы разделов
├── components/
│   ├── App.vue          # рут: loginComp (route.name === 'Login') или admin-layout
│   ├── sideBarComp.vue  # меню разделов + logout
│   ├── headerComp.vue   # заголовок, поиск, фильтр, экспорт
│   ├── bodyComp.vue     # Suspense + переключение table/create/detail
│   ├── loginComp.vue    # форма входа
│   └── subComponents/
│       ├── tableComp.vue    # таблица с пагинацией, retry при сетевой ошибке
│       ├── createComp.vue   # форма создания, загрузка файлов до submit
│       ├── detailsComp.vue  # просмотр/редактирование записи
│       ├── fieldsComps/     # StringComp, NumberComp, DateComp, SelectComp, CheckboxComp, FileComp, DocumentListComp
│       └── createComps/     # аналоги для режима создания
└── assets/
    ├── base.css         # CSS-переменные (тёмная тема, фиолетовый акцент #7867fa)
    └── main.css         # глобальные стили, шрифт Inter
```

## Ключевые паттерны

### Загрузка файлов

Файлы загружаются **до** submit формы через `POST /files` (multipart/form-data). В теле записи хранится возвращённый ID файла.

### Документы пользователя

`DocumentListComp` управляет списком документов. В `detailsComp` реализован ручной диффинг массива документов при обновлении (помечено как "hack" — временное решение).

### Обработка ошибок в API

- **401** → автоматический logout
- **400** → `console.log`
- **остальные** → `alert` + `Promise.reject`
- **сетевая ошибка** в tableComp → retry каждые 10 секунд (очищается при размонтировании)

### Аутентификация

JWT-токен и username хранятся в cookies (`js-cookie`). При login/logout — `location.reload()` для сброса состояния.

## Стиль кода

- Prettier: `semi: false`, одинарные кавычки, 100 символов в строке
- ESLint: flat config, oxlint + eslint-plugin-vue
- `markRaw()` для компонентов внутри реактивных объектов (схемы в sideBar)
- `<style scoped>` во всех компонентах

## Деплой

Dockerfile: multi-stage — Node 22 alpine для сборки, nginx alpine для раздачи.
`vite-plugin-vue-devtools` подключается только в dev-режиме (`mode !== 'production'`).
