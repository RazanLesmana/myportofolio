(() => {
    'use strict';
    const config = document.getElementById('portfolio-api-config').dataset;
    const grid = document.getElementById('grid');
    const search = document.getElementById('search-input');
    const form = document.getElementById(`${config.kind}-form`);
    const owner = config.owner === 'true';
    const authenticated = config.authenticated === 'true';
    const editForm = document.getElementById('experience-edit-form');
    const editModal = document.getElementById('edit-experience-modal');
    const category = document.getElementById('category-filter');
    let editTrigger;
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
                links += `<button type="button" class="button" data-action="edit" data-id="${escapeHtml(item.id)}">Edit</button>`;
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
            if (category) url.searchParams.set('category', category.value);
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
            const error = new Error(errors.join(' ') || `Permintaan gagal (HTTP ${response.status}).`);
            error.fields = data;
            throw error;
        }
        return data;
    }

    function formPayload(target) {
        const payload = {};
        for (const input of target.elements) {
            if (!input.name || input.name === 'csrfmiddlewaretoken' || input.disabled) continue;
            payload[input.name] = input.type === 'checkbox' ? input.checked : input.value;
        }
        return payload;
    }

    function fieldErrors(errors = {}) {
        for (const label of editForm.querySelectorAll('[data-error-for]')) {
            const name = label.dataset.errorFor;
            const messages = errors[name];
            label.textContent = Array.isArray(messages) ? messages.join(' ') : (messages || '');
            const input = editForm.elements.namedItem(name);
            input.setAttribute('aria-invalid', messages ? 'true' : 'false');
            input.setAttribute('aria-describedby', label.id);
        }
    }

    function closeEdit() {
        editModal.hidePopover();
        if (editTrigger?.isConnected) editTrigger.focus();
        else search.focus();
    }

    if (editForm) {
        const save = editForm.querySelector('button[type="submit"]');
        const cancel = document.getElementById('cancel-edit');
        cancel.addEventListener('click', closeEdit);
        editModal.addEventListener('keydown', event => {
            if (event.key === 'Escape' && !save.disabled) { event.preventDefault(); closeEdit(); }
            if (event.key === 'Tab') {
                const controls = [...editForm.elements].filter(input => !input.disabled && input.type !== 'hidden');
                const first = controls[0], last = controls[controls.length - 1];
                if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
                else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
            }
        });
        editForm.addEventListener('submit', async event => {
            event.preventDefault();
            if (save.disabled) return;
            fieldErrors();
            const payload = formPayload(editForm);
            save.disabled = cancel.disabled = true;
            save.textContent = 'Menyimpan...';
            editForm.setAttribute('aria-busy', 'true');
            try {
                await write(endpoint(config.detail, editForm.dataset.id), 'PATCH', payload);
                closeEdit();
                showToast('Berhasil', 'Experience berhasil diperbarui.', 'success');
                await fetchItems();
                search.focus();
            } catch (error) {
                fieldErrors(error.fields);
                showToast('Gagal menyimpan', error.message, 'error');
                editForm.querySelector('[aria-invalid="true"]')?.focus();
            } finally {
                save.disabled = cancel.disabled = false;
                save.textContent = 'Simpan perubahan';
                editForm.setAttribute('aria-busy', 'false');
            }
        });
    }

    if (form) form.addEventListener('submit', async event => {
        event.preventDefault();
        const button = form.querySelector('button[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        try {
            const payload = formPayload(form);
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
        if (button.dataset.action === 'edit') {
            button.disabled = true;
            try {
                // Read the detail endpoint on opening so the form uses current server data.
                const response = await fetch(endpoint(config.detail, button.dataset.id), { headers: { Accept: 'application/json' } });
                if (!response.ok) throw new Error(`Gagal memuat experience (HTTP ${response.status}).`);
                const item = await response.json();
                fieldErrors();
                editForm.dataset.id = item.id;
                for (const input of editForm.elements) {
                    if (!input.name || input.name === 'csrfmiddlewaretoken') continue;
                    if (input.type === 'checkbox') input.checked = Boolean(item[input.name]);
                    else input.value = item[input.name] ?? '';
                }
                editTrigger = button;
                editModal.showPopover();
                editForm.elements.namedItem('title').focus();
            } catch (error) { showToast('Gagal membuka edit', error.message, 'error'); }
            finally { button.disabled = false; }
            return;
        }
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

    document.getElementById('retry-load')?.addEventListener('click', fetchItems);
    category?.addEventListener('change', () => { clearTimeout(debounce); fetchItems(); });
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
