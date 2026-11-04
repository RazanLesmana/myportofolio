const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const source = readFileSync('static/js/portfolio-api.js', 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));

function setup({ owner = false, authenticated = false, responses = [] } = {}) {
    const nodes = {};
    function element(id) {
        return nodes[id] ??= {
            value: '', dataset: {}, events: {}, hidden: true,
            classList: { toggle(name, hidden) { nodes[id].hidden = hidden; } },
            addEventListener(name, callback) { this.events[name] = callback; },
            replaceChildren(...children) { this.children = children; },
        };
    }
    const config = element('portfolio-api-config');
    config.dataset = {
        kind: 'project', list: '/api/v1/projects/',
        detail: '/api/v1/projects/00000000-0000-0000-0000-000000000000/',
        star: '/api/v1/projects/00000000-0000-0000-0000-000000000000/star/',
        login: '/login/', owner: String(owner), authenticated: String(authenticated),
    };
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
            getElementById: id => id === 'project-form' && !owner ? null : element(id),
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
