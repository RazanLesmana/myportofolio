(() => {
    'use strict';
    const config = document.getElementById('portfolio-api-config').dataset;
    const grid = document.getElementById('grid');
    const search = document.getElementById('search-input');
    const form = document.getElementById(`${config.kind}-form`);
    const owner = config.owner === 'true';
    const authenticated = config.authenticated === 'true';
    let controller;
    let debounce;

    function escapeHtml(value) {
        return String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
    }

    // Escaping quotes alone does not make a javascript: URL safe.
    function safeUrl(value) {
        if (!value) return '';
        try {
            const url = new URL(value, window.location.origin);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
        } catch { return ''; }
    }

    function endpoint(pattern, id) {
        return pattern.replace('00000000-0000-0000-0000-000000000000', id);
    }

    function display(state) {
        for (const id of ['loading', 'error', 'empty', 'grid']) {
            document.getElementById(id).classList.toggle('hide', id !== state);
        }
    }

    function card(item) {
        const article = document.createElement('article');
        article.className = 'experience-card';
        let content = '';
        let links = '';
        if (config.kind === 'project') {
            const image = safeUrl(item.image_url);
            content = image ? `<img src="${escapeHtml(image)}" alt="${escapeHtml(item.title)}" class="card-image">` : '';
            content += `<h2>${escapeHtml(item.title)}</h2><span class="experience-category">${escapeHtml(item.project_type_display)}</span>`;
            for (const [url, label] of [[item.link, item.link_label], [item.link_2, item.link_2_label]]) {
                const href = safeUrl(url);
                if (href) links += `<a href="${escapeHtml(href)}" class="button">${escapeHtml(label || 'Lihat proyek')}</a>`;
            }
        } else {
            content = `<h2>${escapeHtml(item.title)}</h2><p>${escapeHtml(item.company)}</p>
                <span class="experience-category">${escapeHtml(item.category_display)}</span>
                <p>${escapeHtml(item.period)} · ${item.is_ongoing ? 'Sedang berlangsung' : 'Selesai'}</p>`;
            if (owner || config.editor === 'true') {
                links += `<a class="button" href="${escapeHtml(endpoint(config.edit, item.id))}">Edit</a>`;
            }
        }
        const star = authenticated
            ? `<button type="button" class="button button-star${item.is_starred ? ' is-starred' : ''}"
                data-action="star" data-id="${escapeHtml(item.id)}" title="${escapeHtml(item.starred_by_names)}">
                ${item.is_starred ? 'Unstar' : 'Star'} (${escapeHtml(item.star_count)})</button>`
            : `<a class="button" href="${escapeHtml(config.login)}">Login untuk star (${escapeHtml(item.star_count)})</a>`;
        const remove = owner ? `<button type="button" class="button button-danger" data-action="delete" data-id="${escapeHtml(item.id)}">Hapus</button>` : '';
        article.innerHTML = `${content}<p class="experience-description">${escapeHtml(item.description)}</p>
            <div class="project-card-actions"><div class="project-actions">${links}${star}${remove}</div></div>`;
        return article;
    }

    async function fetchItems() {
        if (controller) controller.abort();
        const current = new AbortController();
        controller = current;
        display('loading');
        try {
            const url = new URL(config.list, window.location.origin);
            url.searchParams.set('title', search.value.trim());
            const response = await fetch(url, { headers: { Accept: 'application/json' }, signal: current.signal });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const items = await response.json();
            if (current !== controller) return;
            grid.replaceChildren(...items.map(card));
            display(items.length ? 'grid' : 'empty');
        } catch (error) {
            if (error.name !== 'AbortError' && current === controller) display('error');
        }
    }

    async function write(url, method, payload) {
        const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const response = await fetch(url, {
            method,
            headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });
        if (response.status === 204) return null;
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            const errors = Object.entries(data).map(([key, value]) =>
                `${key === 'detail' ? '' : `${key}: `}${Array.isArray(value) ? value.join(' ') : value}`);
            throw new Error(errors.join(' ') || `Permintaan gagal (HTTP ${response.status}).`);
        }
        return data;
    }

    if (form) form.addEventListener('submit', async event => {
        event.preventDefault();
        const button = form.querySelector('button[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        try {
            const payload = {};
            for (const input of form.elements) {
                if (!input.name || input.name === 'csrfmiddlewaretoken' || input.disabled) continue;
                payload[input.name] = input.type === 'checkbox' ? input.checked : input.value;
            }
            await write(config.list, 'POST', payload);
            form.reset();
            document.getElementById(`add-${config.kind}-modal`).hidePopover();
            showToast('Berhasil', 'Data berhasil ditambahkan.', 'success');
            await fetchItems();
        } catch (error) { showToast('Gagal menambahkan data', error.message, 'error'); }
        finally { button.disabled = false; }
    });

    grid.addEventListener('click', async event => {
        const button = event.target.closest('button[data-action]');
        if (!button || button.disabled) return;
        const remove = button.dataset.action === 'delete';
        if (remove && !window.confirm('Yakin ingin menghapus data ini?')) return;
        button.disabled = true;
        try {
            await write(endpoint(remove ? config.detail : config.star, button.dataset.id), remove ? 'DELETE' : 'POST');
            showToast('Berhasil', remove ? 'Data berhasil dihapus.' : 'Star diperbarui.', 'success');
            await fetchItems();
        } catch (error) { showToast('Permintaan gagal', error.message, 'error'); }
        finally { button.disabled = false; }
    });

    search.addEventListener('input', () => {
        if (controller) controller.abort();
        clearTimeout(debounce);
        debounce = setTimeout(fetchItems, 300);
    });
    document.getElementById(`${config.kind}-search-form`).addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(debounce);
        fetchItems();
    });
    fetchItems();
})();
