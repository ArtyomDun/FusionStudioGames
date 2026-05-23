const APPS_JSON = './data/apps.json';

function escapeHtml(value = '') {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function truncate(text, max = 120) {
  if (!text) return '';
  return text.length > max ? `${text.slice(0, max - 1)}...` : text;
}

function renderApps(apps) {
  const root = document.getElementById('apps');
  const status = document.getElementById('status');

  if (!apps.length) {
    status.textContent = 'Пока нет данных по приложениям. Проверьте запуск workflow в GitHub Actions.';
    return;
  }

  status.textContent = `Найдено приложений: ${apps.length}`;

  root.innerHTML = apps.map((app) => {
    const safeTitle = escapeHtml(app.title || 'Untitled');
    const safeDesc = escapeHtml(truncate(app.summary || 'Описание отсутствует'));
    const safeUrl = app.url || '#';
    const safeIcon = app.icon || '';

    return `
      <article class="card">
        <div class="icon-wrap">
          ${safeIcon ? `<img class="icon" src="${safeIcon}" alt="${safeTitle} icon" loading="lazy" />` : ''}
        </div>
        <h2 class="app-name">${safeTitle}</h2>
        <p class="app-desc">${safeDesc}</p>
        <a class="outline-btn app-link" href="${safeUrl}" target="_blank" rel="noopener noreferrer">Открыть в Google Play</a>
      </article>
    `;
  }).join('');
}

async function bootstrap() {
  const status = document.getElementById('status');

  try {
    const res = await fetch(APPS_JSON, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    renderApps(Array.isArray(data.apps) ? data.apps : []);
  } catch (error) {
    status.textContent = 'Не удалось загрузить список приложений.';
    console.error('Failed to load apps.json', error);
  }
}

bootstrap();
