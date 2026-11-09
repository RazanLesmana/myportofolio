const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const source = readFileSync('static/js/portfolio-api.js', 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));

function setup({ owner = false, authenticated = false, kind = 'project', editor = false, responses = [] } = {}) {
    const nodes = {};
    function element(id) {
        return nodes[id] ??= {
            value: '', dataset: {}, events: {}, hidden: true,
            focus() {}, setAttribute() {}, querySelectorAll() { return []; },
            classList: { toggle(name, hidden) { nodes[id].hidden = hidden; } },
            addEventListener(name, callback) { this.events[name] = callback; },
            replaceChildren(...children) { this.children = children; },
        };
    }
    const config = element('portfolio-api-config');
    config.dataset = {
        kind, editor: String(editor), list: `/api/v1/${kind}s/`,
        detail: '/api/v1/projects/00000000-0000-0000-0000-000000000000/',
        star: '/api/v1/projects/00000000-0000-0000-0000-000000000000/star/',
        login: '/login/', owner: String(owner), authenticated: String(authenticated),
    };
    if (kind === 'experience') {
        config.dataset.detail = '/api/v1/experiences/00000000-0000-0000-0000-000000000000/';
        const edit = element('experience-edit-form');
        edit.elements = [{ name: 'title', value: '', focus() {} }, { name: 'is_featured', type: 'checkbox', checked: false }];
        edit.elements.namedItem = name => edit.elements.find(input => input.name === name);
        const save = { disabled: false };
        edit.querySelector = selector => selector.includes('submit') ? save : null;
        const modal = element('edit-experience-modal');
        modal.showPopover = () => { modal.open = true; };
        modal.hidePopover = () => { modal.open = false; };
    }
    let button;
    if (owner) {
        const form = element('project-form');
        button = { disabled: false };
        form.querySelector = () => button;
        form.elements = [{ name: 'title', value: 'New' },
            { name: 'is_featured', type: 'checkbox', checked: false },
            { name: 'csrfmiddlewaretoken', value: 'private-token' }];
        form.reset = () => { form.didReset = true; };
        element('add-project-modal').hidePopover = () => {};
    }
    const requests = [];
    const toasts = [];
    const context = {
        URL, AbortController, setTimeout, clearTimeout,
        window: { location: { origin: 'http://localhost' }, confirm: () => true },
        document: {
            getElementById: id => {
                if (id === `${kind}-form` && !owner) return null;
                if (kind === 'project' && ['experience-edit-form', 'edit-experience-modal', 'category-filter', 'retry-load'].includes(id)) return null;
                return element(id);
            },
            querySelector: () => ({ value: 'csrf-token' }),
            createElement: () => ({}),
        },
        showToast: (...args) => toasts.push(args),
        fetch: async (url, options) => {
            requests.push({ url: String(url), ...options });
            const next = responses.shift() ?? { data: [] };
            if (next instanceof Error) throw next;
            const status = next.status ?? 200;
            return { status, ok: status < 400, json: async () => {
                assert.notEqual(status, 204, 'DELETE must not parse an empty response');
                return next.data;
            } };
        },
    };
    vm.runInNewContext(source, context);
    return { nodes, requests, toasts, button };
}

test('guest cards escape text, reject script URLs, and offer login', async () => {
    const { nodes } = setup({ responses: [{ data: [{ id: 'one', title: '<img onerror="bad()">',
        description: '<script>bad()</script>', link: 'javascript:bad()', image_url: 'javascript:bad()',
        project_type_display: 'Personal', star_count: 0 }] }] });
    await tick();
    const html = nodes.grid.children[0].innerHTML;
    assert.match(html, /&lt;img/);
    assert.doesNotMatch(html, /<script>|javascript:|data-action=/);
    assert.match(html, /Login untuk star/);
    assert.equal(nodes.grid.hidden, false);
});

test('create sends JSON and CSRF, preserving false checkbox values', async () => {
    const { nodes, requests, button } = setup({ owner: true, responses: [
        { data: [] }, { status: 201, data: { id: 'new' } }, { data: [] },
    ] });
    await tick();
    nodes['search-input'].value = 'active search';
    await nodes['project-form'].events.submit({ preventDefault() {} });
    assert.equal(requests[1].method, 'POST');
    assert.equal(requests[1].headers['X-CSRFToken'], 'csrf-token');
    assert.deepEqual(JSON.parse(requests[1].body), { title: 'New', is_featured: false });
    assert.match(requests[2].url, /title=active\+search/);
    assert.equal(nodes['project-form'].didReset, true);
    assert.equal(button.disabled, false);
});

test('DELETE accepts 204 without parsing JSON and refreshes list', async () => {
    const { nodes, requests } = setup({ owner: true, responses: [
        { data: [] }, { status: 204 }, { data: [] },
    ] });
    await tick();
    const button = { dataset: { action: 'delete', id: 'one' }, disabled: false };
    await nodes.grid.events.click({ target: { closest: () => button } });
    assert.equal(requests[1].method, 'DELETE');
    assert.equal(requests[1].url, '/api/v1/projects/one/');
    assert.equal(requests.length, 3);
    assert.equal(button.disabled, false);
});

test('serializer errors preserve the form and re-enable submission', async () => {
    const { nodes, toasts, button } = setup({ owner: true, responses: [
        { data: [] }, { status: 400, data: { title: ['Cannot be blank.'] } },
    ] });
    await tick();
    await nodes['project-form'].events.submit({ preventDefault() {} });
    assert.match(toasts[0][1], /title: Cannot be blank/);
    assert.equal(nodes['project-form'].didReset, undefined);
    assert.equal(button.disabled, false);
});

test('network failure shows error state', async () => {
    const { nodes } = setup({ responses: [new Error('offline')] });
    await tick();
    assert.equal(nodes.error.hidden, false);
    assert.equal(nodes.loading.hidden, true);
});


test('editor loads current detail and PATCHes JSON with CSRF without resetting filters', async () => {
    const { nodes, requests } = setup({ kind: 'experience', editor: true, authenticated: true, responses: [
        { data: [] }, { data: { id: 'one', title: '<b>Developer</b>', is_featured: true } },
        { data: { id: 'one' } }, { data: [] },
    ] });
    await tick();
    const trigger = { dataset: { action: 'edit', id: 'one' }, disabled: false };
    await nodes.grid.events.click({ target: { closest: () => trigger } });
    const edit = nodes['experience-edit-form'];
    assert.equal(edit.elements[0].value, '<b>Developer</b>');
    assert.equal(edit.elements[1].checked, true);
    assert.equal(nodes['edit-experience-modal'].open, true);
    edit.elements[0].value = 'Updated';
    edit.elements[1].checked = false;
    nodes['category-filter'].value = 'internship';
    await edit.events.submit({ preventDefault() {} });
    assert.equal(requests[2].method, 'PATCH');
    assert.equal(requests[2].headers['X-CSRFToken'], 'csrf-token');
    assert.deepEqual(JSON.parse(requests[2].body), { title: 'Updated', is_featured: false });
    assert.equal(nodes['edit-experience-modal'].open, false);
    assert.match(requests[3].url, /category=internship/);
});

for (const status of [400, 403]) test(`edit ${status} keeps draft and shows toast`, async () => {
    const { nodes, toasts } = setup({ kind: 'experience', editor: true, responses: [
        { data: [] }, { data: { id: 'one', title: 'Developer' } },
        { status, data: { title: ['Cannot save'] } },
    ] });
    await tick();
    await nodes.grid.events.click({ target: { closest: () => ({ dataset: { action: 'edit', id: 'one' } }) } });
    const edit = nodes['experience-edit-form'];
    edit.elements[0].value = 'My draft';
    await edit.events.submit({ preventDefault() {} });
    assert.equal(edit.elements[0].value, 'My draft');
    assert.equal(nodes['edit-experience-modal'].open, true);
    assert.equal(edit.querySelector('submit').disabled, false);
    assert.match(toasts[0][1], /Cannot save/);
});

test('retry recovers a failed experience list', async () => {
    const { nodes, requests } = setup({ kind: 'experience', responses: [new Error('offline'), { data: [] }] });
    await tick();
    assert.equal(nodes.error.hidden, false);
    await nodes['retry-load'].events.click();
    assert.equal(requests.length, 2);
    assert.equal(nodes.empty.hidden, false);
});
