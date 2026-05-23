# Indie Dev Google Play Site

Простой статический сайт для GitHub Pages:
- логотип из проекта (`text logo.png`)
- список игр карточками
- кнопки с белым outline
- автогенерация `data/apps.json` из Google Play developer page

## Файлы
- `index.html` — разметка
- `styles.css` — черный стиль + белые outlines
- `script.js` — рендер карточек из JSON
- `scripts/fetch_play_apps.py` — парсинг Google Play
- `.github/workflows/update-apps.yml` — автообновление данных

## Публикация в GitHub Pages
1. Загрузите проект в GitHub репозиторий.
2. В `Settings -> Pages` выберите:
   - `Source: Deploy from a branch`
   - `Branch: main` и `/ (root)`
3. Откройте `Actions -> Update Google Play Apps Data` и нажмите `Run workflow`.
4. После первого запуска проверьте `data/apps.json`: там появятся приложения.

## Автообновление
Workflow обновляет карточки автоматически каждый понедельник в `06:00 UTC`.
