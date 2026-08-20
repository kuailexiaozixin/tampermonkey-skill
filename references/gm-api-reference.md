# GM API 参考

> Tampermonkey / ScriptCat 全部 GM API 参考：GM.* 异步与 GM_* 同步风格、存储、Cookie、标签页、音频、DOM 与 UI、HTTP 与 Web 请求拦截、ScriptCat 特有 API，以及 ScriptCat 开发助手。

## Tampermonkey Async API Reference

Documentation for GM.* promise-based functions.

---

### Overview

The GM.* API provides promise-based versions of GM_* functions. Use with async/await for cleaner code.

**Key differences from GM_* functions:**
- Return Promises instead of values/callbacks
- Use `await` or `.then()` for results
- Some have slightly different names (note capitalisation)

---

### Naming Conventions

| Sync (GM_*) | Async (GM.*) | Note |
|-------------|--------------|------|
| `GM_getValue` | `GM.getValue` | Same name |
| `GM_setValue` | `GM.setValue` | Same name |
| `GM_deleteValue` | `GM.deleteValue` | Same name |
| `GM_listValues` | `GM.listValues` | Same name |
| `GM_getResourceURL` | `GM.getResourceUrl` | Note: lowercase "r" and "l" |
| `GM_xmlhttpRequest` | `GM.xmlHttpRequest` | Note: uppercase "H" |
| `GM_notification` | `GM.notification` | Returns boolean (was clicked) |
| `GM_setClipboard` | `GM.setClipboard` | Returns Promise<void> |

---

### Storage Functions

#### GM.getValue(key, defaultValue)

```javascript
// @grant GM.getValue

const username = await GM.getValue('username', 'Anonymous');
const settings = await GM.getValue('settings', { theme: 'dark', lang: 'en' });
```

#### GM.setValue(key, value)

```javascript
// @grant GM.setValue

await GM.setValue('username', 'John');
await GM.setValue('settings', { theme: 'light', lang: 'fr' });
await GM.setValue('lastVisit', Date.now());
```

#### GM.deleteValue(key)

```javascript
// @grant GM.deleteValue

await GM.deleteValue('tempData');
```

#### GM.listValues()

```javascript
// @grant GM.listValues

const keys = await GM.listValues();
console.log('Stored keys:', keys);
```

#### GM.getValues(keysOrDefaults) (v5.3+)

```javascript
// @grant GM.getValues

// With array of keys
const values = await GM.getValues(['foo', 'bar', 'baz']);

// With default values
const values2 = await GM.getValues({
    foo: 1,
    bar: 'default',
    baz: null
});
```

#### GM.setValues(values) (v5.3+)

```javascript
// @grant GM.setValues

await GM.setValues({
    username: 'John',
    theme: 'dark',
    lastLogin: Date.now()
});
```

#### GM.deleteValues(keys) (v5.3+)

```javascript
// @grant GM.deleteValues

await GM.deleteValues(['tempData', 'cache', 'oldSettings']);
```

#### GM.addValueChangeListener(key, callback)

```javascript
// @grant GM.addValueChangeListener

const listenerId = await GM.addValueChangeListener('counter', (key, oldValue, newValue, remote) => {
    console.log(`${key} changed from ${oldValue} to ${newValue}`);
    if (remote) {
        console.log('Change came from another tab');
    }
});
```

#### GM.removeValueChangeListener(listenerId)

```javascript
// @grant GM.removeValueChangeListener

await GM.removeValueChangeListener(listenerId);
```

---

### Resource Functions

#### GM.getResourceText(name)

```javascript
// @resource myCSS https://example.com/style.css
// @grant GM.getResourceText

const cssText = await GM.getResourceText('myCSS');
```

#### GM.getResourceUrl(name)

**Note:** Lowercase "r" and "l" in "Url" (different from sync version).

```javascript
// @resource myIcon https://example.com/icon.png
// @grant GM.getResourceUrl

const iconUrl = await GM.getResourceUrl('myIcon');
img.src = iconUrl;
```

---

### Network Requests

#### GM.xmlHttpRequest(details)

**Note:** Uppercase "H" in "Http" (different from sync version).

```javascript
// @grant GM.xmlHttpRequest
// @connect api.example.com

try {
    const response = await GM.xmlHttpRequest({
        method: 'GET',
        url: 'https://api.example.com/data',
        headers: {
            'Accept': 'application/json'
        }
    });

    const data = JSON.parse(response.responseText);
    console.log(data);
} catch (error) {
    console.error('Request failed:', error);
}
```

The promise also has an `abort()` function:

```javascript
const request = GM.xmlHttpRequest({
    method: 'GET',
    url: 'https://api.example.com/large-file'
});

// Cancel after 5 seconds
setTimeout(() => request.abort(), 5000);

try {
    const response = await request;
} catch (error) {
    console.log('Request was aborted or failed');
}
```

---

### UI Functions

#### GM.notification(details)

Returns a Promise that resolves to `true` if clicked, `false` otherwise.

```javascript
// @grant GM.notification

const wasClicked = await GM.notification({
    text: 'Click me!',
    title: 'Notification',
    timeout: 10000
});

if (wasClicked) {
    console.log('User clicked the notification');
} else {
    console.log('Notification timed out or was dismissed');
}
```

#### GM.setClipboard(data, type)

```javascript
// @grant GM.setClipboard

await GM.setClipboard('Copied text', 'text');
console.log('Text copied to clipboard');
```

---

### Tab Functions

#### GM.getTab()

```javascript
// @grant GM.getTab

const tab = await GM.getTab();
console.log('Tab data:', tab);
```

#### GM.saveTab(tab)

```javascript
// @grant GM.saveTab

const tab = await GM.getTab();
tab.customData = { lastAction: 'click', timestamp: Date.now() };
await GM.saveTab(tab);
```

#### GM.getTabs()

```javascript
// @grant GM.getTabs

const tabs = await GM.getTabs();
for (const [tabId, tabData] of Object.entries(tabs)) {
    console.log(`Tab ${tabId}:`, tabData);
}
```

---

### Cookie Functions

#### GM.cookie.list(details)

```javascript
// @grant GM.cookie

const cookies = await GM.cookie.list({ domain: 'example.com' });
console.log('Cookies:', cookies);
```

#### GM.cookie.set(details)

```javascript
// @grant GM.cookie

await GM.cookie.set({
    name: 'myCookie',
    value: 'myValue',
    domain: 'example.com',
    path: '/',
    secure: true
});
```

#### GM.cookie.delete(details)

```javascript
// @grant GM.cookie

await GM.cookie.delete({ name: 'myCookie' });
```

---

### Audio Functions (v5.0+)

#### GM.audio.setMute(details)

```javascript
// @grant GM.audio

await GM.audio.setMute({ isMuted: true });
console.log('Tab muted');
```

#### GM.audio.getState()

```javascript
// @grant GM.audio

const state = await GM.audio.getState();
console.log(`Muted: ${state.isMuted}, Audible: ${state.isAudible}`);
```

#### GM.audio.addStateChangeListener(listener)

```javascript
// @grant GM.audio

await GM.audio.addStateChangeListener((event) => {
    if ('muted' in event) console.log('Mute changed:', event.muted);
    if ('audible' in event) console.log('Audible changed:', event.audible);
});
```

---

### Combining Async Operations

#### Sequential Operations

```javascript
async function loadUserData() {
    const userId = await GM.getValue('userId');
    const response = await GM.xmlHttpRequest({
        url: `https://api.example.com/users/${userId}`
    });
    const userData = JSON.parse(response.responseText);
    await GM.setValue('userData', userData);
    return userData;
}
```

#### Parallel Operations

```javascript
async function loadAllSettings() {
    const [theme, language, notifications] = await Promise.all([
        GM.getValue('theme', 'dark'),
        GM.getValue('language', 'en'),
        GM.getValue('notifications', true)
    ]);

    return { theme, language, notifications };
}
```

#### Error Handling

```javascript
async function safeRequest(url) {
    try {
        const response = await GM.xmlHttpRequest({
            method: 'GET',
            url: url,
            timeout: 5000
        });
        return JSON.parse(response.responseText);
    } catch (error) {
        console.error('Request failed:', error);
        await GM.notification({
            text: 'Failed to load data',
            title: 'Error'
        });
        return null;
    }
}
```

---

## Tampermonkey Synchronous API Reference

Documentation for all GM_* synchronous functions.

---

### GM_info

Get information about the script and Tampermonkey. No @grant required.

```javascript
console.log(GM_info.script.name);        // Script name
console.log(GM_info.script.version);     // Script version
console.log(GM_info.scriptHandler);      // "Tampermonkey"
console.log(GM_info.version);            // Tampermonkey version
```

**Key properties:**

| Property | Type | Description |
|----------|------|-------------|
| `script.name` | string | Script name |
| `script.version` | string | Script version |
| `script.description` | string | Script description |
| `script.namespace` | string | Script namespace |
| `script.matches` | string[] | @match patterns |
| `script.includes` | string[] | @include patterns |
| `script.excludes` | string[] | @exclude patterns |
| `script.grant` | string[] | Granted permissions |
| `scriptHandler` | string | "Tampermonkey" |
| `version` | string | Tampermonkey version |
| `isIncognito` | boolean | Running in private mode |
| `sandboxMode` | string | 'js', 'raw', or 'dom' |
| `downloadMode` | string | 'native', 'disabled', or 'browser' |

---

### GM_log(message)

Log a message to the console.

```javascript
// @grant GM_log

GM_log('Debug message');
GM_log('User ID: ' + userId);
```

---

### GM_addStyle(css)

Add CSS styles to the document. Returns the injected style element.

```javascript
// @grant GM_addStyle

// Add styles
const styleElement = GM_addStyle(`
    .my-class {
        background: #f0f0f0;
        padding: 10px;
    }

    #hide-element {
        display: none !important;
    }

    body {
        font-family: 'Arial', sans-serif !important;
    }
`);
```

---

### GM_addElement(tag_name, attributes)
### GM_addElement(parent_node, tag_name, attributes)

Create and inject HTML elements, bypassing CSP restrictions.

```javascript
// @grant GM_addElement

// Add script to page
GM_addElement('script', {
    textContent: 'window.myVar = "injected";'
});

// Add external script
GM_addElement('script', {
    src: 'https://example.com/script.js',
    type: 'text/javascript'
});

// Add image to specific parent
GM_addElement(document.body, 'img', {
    src: 'https://example.com/image.png',
    alt: 'My Image'
});

// Add style to shadow DOM
GM_addElement(shadowRoot, 'style', {
    textContent: 'div { color: blue; }'
});
```

**Returns:** The injected HTML element.

---

### GM_notification(details, ondone)
### GM_notification(text, title, image, onclick)

Display desktop notifications.

**Object syntax:**

```javascript
// @grant GM_notification

GM_notification({
    text: 'Download complete!',
    title: 'My Script',
    image: 'https://example.com/icon.png',
    timeout: 5000,                    // Auto-close after 5 seconds
    silent: false,                    // Play sound
    highlight: false,                 // Highlight tab
    url: 'https://example.com/',      // Open on click (v5.0+)
    tag: 'download-notification',     // Update existing (v5.0+)
    onclick: (event) => {
        event.preventDefault();       // Prevent URL opening
        console.log('Clicked!');
    },
    ondone: () => {
        console.log('Notification closed');
    }
});
```

**Simple syntax:**

```javascript
GM_notification('Message', 'Title', 'https://example.com/icon.png', () => {
    console.log('Clicked!');
});
```

**Parameters:**

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | Notification message |
| `title` | string | Notification title |
| `image` | string | Icon URL |
| `timeout` | number | Auto-close time in ms |
| `silent` | boolean | Suppress sound |
| `highlight` | boolean | Flash the tab |
| `url` | string | URL to open on click (v5.0+) |
| `tag` | string | Unique ID for updating (v5.0+) |
| `onclick` | function | Click handler |
| `ondone` | function | Close handler |

---

### GM_openInTab(url, options)
### GM_openInTab(url, loadInBackground)

Open a new browser tab.

```javascript
// @grant GM_openInTab

// Simple usage
GM_openInTab('https://example.com/');

// With options
const tab = GM_openInTab('https://example.com/', {
    active: true,        // Focus the new tab
    insert: true,        // Insert next to current tab
    setParent: true,     // Set current tab as parent
    incognito: false,    // Open in incognito
    loadInBackground: false  // Legacy: opposite of active
});

// Close the tab later
tab.close();

// Listen for tab close
tab.onclose = () => console.log('Tab closed');
```

**Returns:** Object with `close()` function, `onclose` listener, and `closed` flag.

---

### GM_registerMenuCommand(name, callback, options_or_accessKey)

Add an entry to Tampermonkey's menu.

```javascript
// @grant GM_registerMenuCommand

// Simple usage
const menuId = GM_registerMenuCommand('Say Hello', () => {
    alert('Hello!');
});

// With options (v4.20+)
const menuId2 = GM_registerMenuCommand('Toggle Feature', (event) => {
    console.log('Clicked with:', event);
}, {
    accessKey: 't',       // Keyboard shortcut
    autoClose: true,      // Close menu after click
    title: 'Enable or disable the feature',  // Tooltip (v5.0+)
    id: existingId        // Update existing command (v5.0+)
});

// With just access key (legacy)
const menuId3 = GM_registerMenuCommand('Quick Action', callback, 'q');
```

**Returns:** Menu command ID for later removal.

---

### GM_unregisterMenuCommand(menuCmdId)

Remove a menu command.

```javascript
// @grant GM_unregisterMenuCommand

const menuId = GM_registerMenuCommand('Temporary', callback);
// Later...
GM_unregisterMenuCommand(menuId);
```

---

### GM_setClipboard(data, info, cb)

Copy data to the clipboard.

```javascript
// @grant GM_setClipboard

// Copy text
GM_setClipboard('Hello, World!', 'text');

// Copy HTML
GM_setClipboard('<b>Bold text</b>', 'html');

// With callback
GM_setClipboard('Copied text', 'text', () => {
    console.log('Clipboard set!');
});

// With full info object
GM_setClipboard('Data', {
    type: 'text',
    mimetype: 'text/plain'
});
```

---

### GM_download(details)
### GM_download(url, name)

Download a file.

```javascript
// @grant GM_download

// Simple download
GM_download('https://example.com/file.pdf', 'document.pdf');

// With options
const download = GM_download({
    url: 'https://example.com/file.zip',
    name: 'archive.zip',
    saveAs: true,              // Prompt for location
    headers: {
        'Authorization': 'Bearer token123'
    },
    onload: () => console.log('Complete!'),
    onerror: (error) => console.error('Failed:', error.error),
    onprogress: (progress) => console.log(`${progress.loaded}/${progress.total}`),
    ontimeout: () => console.log('Timed out')
});

// Cancel download
download.abort();
```

**Note:** File extensions must be whitelisted in Tampermonkey options.

**Error types:**
- `not_enabled` - Download feature disabled
- `not_whitelisted` - Extension not allowed
- `not_permitted` - Missing permission
- `not_supported` - Browser doesn't support
- `not_succeeded` - Download failed

---

### GM_getResourceText(name)

Get text content of a preloaded @resource.

```javascript
// @resource myCSS https://example.com/style.css
// @grant GM_getResourceText
// @grant GM_addStyle

const css = GM_getResourceText('myCSS');
GM_addStyle(css);
```

---

### GM_getResourceURL(name)

Get a data URL for a preloaded @resource.

```javascript
// @resource myIcon https://example.com/icon.png
// @grant GM_getResourceURL

const iconUrl = GM_getResourceURL('myIcon');
const img = document.createElement('img');
img.src = iconUrl;
document.body.appendChild(img);
```

---

### unsafeWindow

Access the page's actual window object (not the sandbox).

```javascript
// @grant unsafeWindow

// Access page variables
console.log(unsafeWindow.pageConfig);

// Call page functions
unsafeWindow.showModal('Hello from userscript!');

// Modify page globals
unsafeWindow.DEBUG_MODE = true;
```

**Warning:** Use carefully - can break if page structure changes.

---

## Tampermonkey Storage API Reference

Complete documentation for persistent data storage functions.

---

### Overview

Tampermonkey provides a key-value storage system that:
- Persists across page reloads and browser sessions
- Is isolated per script (scripts can't access each other's data)
- Supports any JSON-serialisable value type
- Can notify listeners of changes across tabs

---

### Single Value Operations

#### GM_setValue(key, value)

Store a value. Supports strings, numbers, booleans, objects, arrays, null, and undefined.

```javascript
// @grant GM_setValue

// Primitive values
GM_setValue('username', 'John');
GM_setValue('count', 42);
GM_setValue('enabled', true);
GM_setValue('lastVisit', Date.now());

// Objects and arrays
GM_setValue('settings', {
    theme: 'dark',
    fontSize: 14,
    notifications: true
});

GM_setValue('history', ['page1', 'page2', 'page3']);

// Nested objects work too
GM_setValue('userData', {
    profile: { name: 'John', age: 30 },
    preferences: { lang: 'en', timezone: 'UTC' }
});
```

#### GM_getValue(key, defaultValue)

Retrieve a value. Returns defaultValue if key doesn't exist.

```javascript
// @grant GM_getValue

const username = GM_getValue('username', 'Guest');
const count = GM_getValue('count', 0);
const settings = GM_getValue('settings', { theme: 'light' });

// Check if value exists
const value = GM_getValue('maybeExists');
if (value === undefined) {
    console.log('Key does not exist');
}
```

#### GM_deleteValue(key)

Remove a stored value.

```javascript
// @grant GM_deleteValue

GM_deleteValue('temporaryData');
GM_deleteValue('cache');
```

#### GM_listValues()

Get an array of all stored keys.

```javascript
// @grant GM_listValues

const keys = GM_listValues();
console.log('Stored keys:', keys);
// ['username', 'settings', 'history']

// Iterate all stored data
keys.forEach(key => {
    console.log(key, '=', GM_getValue(key));
});
```

---

### Batch Operations (v5.3+)

More efficient for multiple operations - reduces overhead.

#### GM_setValues(values)

Store multiple values at once.

```javascript
// @grant GM_setValues

GM_setValues({
    username: 'John',
    theme: 'dark',
    lastLogin: Date.now(),
    settings: { notifications: true, sound: false }
});
```

#### GM_getValues(keysOrDefaults)

Retrieve multiple values at once.

```javascript
// @grant GM_getValues

// With array - returns object with keys (undefined for missing)
const values = GM_getValues(['username', 'theme', 'nonexistent']);
// { username: 'John', theme: 'dark', nonexistent: undefined }

// With defaults object - missing keys get default values
const values2 = GM_getValues({
    username: 'Guest',
    theme: 'light',
    notifications: true
});
// { username: 'John', theme: 'dark', notifications: true }
```

#### GM_deleteValues(keys)

Delete multiple values at once.

```javascript
// @grant GM_deleteValues

GM_deleteValues(['cache', 'tempData', 'oldSettings']);
```

---

### Change Listeners

Listen for value changes, including from other tabs/windows.

#### GM_addValueChangeListener(key, callback)

```javascript
// @grant GM_addValueChangeListener

const listenerId = GM_addValueChangeListener('counter', (key, oldValue, newValue, remote) => {
    console.log(`Key: ${key}`);
    console.log(`Old value: ${oldValue}`);
    console.log(`New value: ${newValue}`);
    console.log(`Remote change: ${remote}`);  // true if from another tab

    if (remote) {
        // Another tab changed this value
        updateUI(newValue);
    }
});
```

**Callback parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | string | The key that changed |
| `oldValue` | any | Previous value |
| `newValue` | any | New value |
| `remote` | boolean | true if change was from another tab |

#### GM_removeValueChangeListener(listenerId)

```javascript
// @grant GM_removeValueChangeListener

GM_removeValueChangeListener(listenerId);
```

---

### Common Patterns

#### Settings Manager

```javascript
// @grant GM_getValue
// @grant GM_setValue
// @grant GM_registerMenuCommand

const DEFAULT_SETTINGS = {
    enabled: true,
    theme: 'auto',
    fontSize: 14,
    notifications: true
};

class Settings {
    constructor() {
        this.data = GM_getValue('settings', DEFAULT_SETTINGS);
    }

    get(key) {
        return this.data[key] ?? DEFAULT_SETTINGS[key];
    }

    set(key, value) {
        this.data[key] = value;
        GM_setValue('settings', this.data);
    }

    reset() {
        this.data = { ...DEFAULT_SETTINGS };
        GM_setValue('settings', this.data);
    }
}

const settings = new Settings();

// Menu commands
GM_registerMenuCommand('Toggle Feature', () => {
    settings.set('enabled', !settings.get('enabled'));
    location.reload();
});
```

#### Cache with Expiry

```javascript
// @grant GM_getValue
// @grant GM_setValue

function getCached(key, fetchFn, maxAgeMs = 3600000) {
    const cached = GM_getValue(`cache_${key}`);

    if (cached && Date.now() - cached.timestamp < maxAgeMs) {
        return Promise.resolve(cached.data);
    }

    return fetchFn().then(data => {
        GM_setValue(`cache_${key}`, {
            data: data,
            timestamp: Date.now()
        });
        return data;
    });
}

// Usage
getCached('userData', () => fetchUserData(), 60000)  // 1 minute cache
    .then(data => console.log(data));
```

#### Cross-Tab Communication

```javascript
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_addValueChangeListener

// Tab 1: Send message
function broadcast(channel, message) {
    GM_setValue(`broadcast_${channel}`, {
        message: message,
        timestamp: Date.now(),
        sender: GM_getValue('tabId', Math.random().toString(36))
    });
}

// Tab 2: Receive messages
GM_addValueChangeListener('broadcast_main', (key, oldVal, newVal, remote) => {
    if (remote && newVal) {
        console.log('Received:', newVal.message);
        handleMessage(newVal.message);
    }
});

// Send a message
broadcast('main', { action: 'refresh', data: { userId: 123 } });
```

#### Migration Between Versions

```javascript
// @grant GM_getValue
// @grant GM_setValue
// @grant GM_deleteValue

const CURRENT_VERSION = 3;

function migrateStorage() {
    const version = GM_getValue('storageVersion', 1);

    if (version < 2) {
        // v1 -> v2: Rename key
        const oldData = GM_getValue('userData');
        if (oldData) {
            GM_setValue('user', oldData);
            GM_deleteValue('userData');
        }
    }

    if (version < 3) {
        // v2 -> v3: Convert settings format
        const settings = GM_getValue('settings', {});
        if (typeof settings.theme === 'boolean') {
            settings.theme = settings.theme ? 'dark' : 'light';
            GM_setValue('settings', settings);
        }
    }

    GM_setValue('storageVersion', CURRENT_VERSION);
}

migrateStorage();
```

#### Persistent Counter

```javascript
// @grant GM_getValue
// @grant GM_setValue

function incrementCounter(key, amount = 1) {
    const current = GM_getValue(key, 0);
    const newValue = current + amount;
    GM_setValue(key, newValue);
    return newValue;
}

// Track page visits
const visitCount = incrementCounter('pageVisits');
console.log(`You've visited this page ${visitCount} times`);
```

---

### Data Types and Limits

#### Supported Types

| Type | Support | Notes |
|------|---------|-------|
| string | Yes | No size limit (practical) |
| number | Yes | Including floats, Infinity, NaN |
| boolean | Yes | |
| null | Yes | |
| undefined | Yes | |
| object | Yes | Must be JSON-serialisable |
| array | Yes | Must be JSON-serialisable |
| Date | Partial | Stored as string, retrieve with new Date() |
| Map/Set | No | Convert to array/object first |
| Function | No | Cannot be serialised |
| Symbol | No | Cannot be serialised |

#### Handling Non-Serialisable Data

```javascript
// Date objects
GM_setValue('lastUpdate', new Date().toISOString());
const date = new Date(GM_getValue('lastUpdate'));

// Map
const map = new Map([['a', 1], ['b', 2]]);
GM_setValue('myMap', Array.from(map.entries()));
const restored = new Map(GM_getValue('myMap'));

// Set
const set = new Set([1, 2, 3]);
GM_setValue('mySet', Array.from(set));
const restoredSet = new Set(GM_getValue('mySet'));
```

---

### Async Versions

All storage functions have GM.* async equivalents. See [api-async.md](api-async.md).

```javascript
// Async equivalents
const value = await GM.getValue('key', 'default');
await GM.setValue('key', 'value');
await GM.deleteValue('key');
const keys = await GM.listValues();
await GM.setValues({ a: 1, b: 2 });
const values = await GM.getValues(['a', 'b']);
await GM.deleteValues(['a', 'b']);
```

---

## Tampermonkey Cookie API Reference

Documentation for browser cookie manipulation functions.

---

### Overview

The GM_cookie API allows userscripts to:
- List cookies from any domain (with @match/@include access)
- Set cookies with full control over attributes
- Delete cookies

**Note:** httpOnly cookies are supported in BETA versions only.

**Required grant:**
```javascript
// @grant GM_cookie
```

---

### GM_cookie.list(details[, callback])

Retrieve cookies matching specified criteria.

#### Basic Usage

```javascript
// @grant GM_cookie

// List all cookies for current domain
GM_cookie.list({}, function(cookies, error) {
    if (error) {
        console.error('Error:', error);
        return;
    }
    console.log('Cookies:', cookies);
});

// Async version
const cookies = await GM.cookie.list();
```

#### Filter Options

```javascript
// By domain
GM_cookie.list({ domain: 'example.com' }, callback);

// By name
GM_cookie.list({ name: 'sessionId' }, callback);

// By path
GM_cookie.list({ path: '/app' }, callback);

// By URL
GM_cookie.list({ url: 'https://example.com/page' }, callback);

// Partitioned cookies (v5.2+)
GM_cookie.list({
    partitionKey: { topLevelSite: 'https://example.com' }
}, callback);

// All cookies (empty partitionKey)
GM_cookie.list({ partitionKey: {} }, callback);
```

#### Cookie Object Properties

```javascript
GM_cookie.list({}, (cookies, error) => {
    cookies.forEach(cookie => {
        console.log(cookie.name);           // Cookie name
        console.log(cookie.value);          // Cookie value
        console.log(cookie.domain);         // Domain (e.g., ".example.com")
        console.log(cookie.path);           // Path (e.g., "/")
        console.log(cookie.secure);         // HTTPS only
        console.log(cookie.httpOnly);       // Not accessible via JS
        console.log(cookie.sameSite);       // "strict", "lax", "none"
        console.log(cookie.session);        // Session cookie (no expiry)
        console.log(cookie.expirationDate); // Unix timestamp (seconds)
        console.log(cookie.hostOnly);       // Exact domain match only
        console.log(cookie.firstPartyDomain); // First-party isolation
    });
});
```

---

### GM_cookie.set(details[, callback])

Create or update a cookie.

#### Basic Usage

```javascript
// @grant GM_cookie

// Simple cookie
GM_cookie.set({
    name: 'myCookie',
    value: 'myValue'
}, function(error) {
    if (error) {
        console.error('Failed to set cookie:', error);
    } else {
        console.log('Cookie set!');
    }
});

// Async version
await GM.cookie.set({ name: 'myCookie', value: 'myValue' });
```

#### Full Options

```javascript
GM_cookie.set({
    // Required
    name: 'sessionToken',
    value: 'abc123xyz',

    // Optional - domain and path
    url: 'https://example.com',           // URL to associate with
    domain: '.example.com',               // Cookie domain
    path: '/',                            // Cookie path

    // Optional - security
    secure: true,                         // HTTPS only
    httpOnly: true,                       // Not accessible via JS
    sameSite: 'strict',                   // "strict", "lax", "none"

    // Optional - expiry
    expirationDate: Math.floor(Date.now() / 1000) + 86400,  // 24 hours

    // Optional - partitioning (v5.2+)
    partitionKey: {
        topLevelSite: 'https://example.com'
    },

    // Optional - first-party isolation
    firstPartyDomain: 'example.com'
}, callback);
```

#### Cookie Expiry Examples

```javascript
// Session cookie (no expirationDate)
GM_cookie.set({ name: 'session', value: 'temp' });

// Expire in 1 hour
GM_cookie.set({
    name: 'hourly',
    value: 'data',
    expirationDate: Math.floor(Date.now() / 1000) + 3600
});

// Expire in 30 days
GM_cookie.set({
    name: 'monthly',
    value: 'data',
    expirationDate: Math.floor(Date.now() / 1000) + (30 * 24 * 60 * 60)
});

// Expire at specific date
GM_cookie.set({
    name: 'endOfYear',
    value: 'data',
    expirationDate: new Date('2025-12-31').getTime() / 1000
});
```

---

### GM_cookie.delete(details, callback)

Remove a cookie.

#### Basic Usage

```javascript
// @grant GM_cookie

GM_cookie.delete({ name: 'myCookie' }, function(error) {
    if (error) {
        console.error('Failed to delete:', error);
    } else {
        console.log('Cookie deleted');
    }
});

// Async version
await GM.cookie.delete({ name: 'myCookie' });
```

#### Delete Options

```javascript
GM_cookie.delete({
    name: 'sessionToken',
    url: 'https://example.com',           // URL associated with cookie
    firstPartyDomain: 'example.com',      // First-party isolation
    partitionKey: {                       // Partitioned cookies (v5.2+)
        topLevelSite: 'https://example.com'
    }
}, callback);
```

---

### Common Patterns

#### Read and Modify Cookie

```javascript
async function updateCookie(name, modifier) {
    const cookies = await GM.cookie.list({ name });

    if (cookies.length === 0) {
        console.log('Cookie not found');
        return;
    }

    const cookie = cookies[0];
    const newValue = modifier(cookie.value);

    await GM.cookie.set({
        name: cookie.name,
        value: newValue,
        domain: cookie.domain,
        path: cookie.path,
        secure: cookie.secure,
        expirationDate: cookie.expirationDate
    });

    return newValue;
}

// Usage: increment a counter cookie
updateCookie('visitCount', val => String(parseInt(val || '0') + 1));
```

#### Cookie Manager Class

```javascript
class CookieManager {
    constructor(domain) {
        this.domain = domain;
    }

    async get(name) {
        const cookies = await GM.cookie.list({ domain: this.domain, name });
        return cookies.length > 0 ? cookies[0].value : null;
    }

    async set(name, value, options = {}) {
        await GM.cookie.set({
            name,
            value,
            domain: this.domain,
            path: options.path || '/',
            secure: options.secure ?? true,
            expirationDate: options.expiresIn
                ? Math.floor(Date.now() / 1000) + options.expiresIn
                : undefined
        });
    }

    async delete(name) {
        await GM.cookie.delete({ name, domain: this.domain });
    }

    async getAll() {
        return await GM.cookie.list({ domain: this.domain });
    }

    async clear() {
        const cookies = await this.getAll();
        for (const cookie of cookies) {
            await this.delete(cookie.name);
        }
    }
}

// Usage
const cookies = new CookieManager('example.com');
await cookies.set('theme', 'dark', { expiresIn: 86400 * 30 });
const theme = await cookies.get('theme');
```

#### Backup and Restore Cookies

```javascript
async function backupCookies(domain) {
    const cookies = await GM.cookie.list({ domain });
    GM_setValue('cookieBackup', cookies);
    return cookies.length;
}

async function restoreCookies() {
    const backup = GM_getValue('cookieBackup', []);
    for (const cookie of backup) {
        await GM.cookie.set({
            name: cookie.name,
            value: cookie.value,
            domain: cookie.domain,
            path: cookie.path,
            secure: cookie.secure,
            httpOnly: cookie.httpOnly,
            sameSite: cookie.sameSite,
            expirationDate: cookie.expirationDate
        });
    }
    return backup.length;
}
```

#### Session Hijacking Prevention Check

```javascript
async function checkSessionSecurity() {
    const cookies = await GM.cookie.list({});
    const issues = [];

    for (const cookie of cookies) {
        if (cookie.name.toLowerCase().includes('session') ||
            cookie.name.toLowerCase().includes('token')) {

            if (!cookie.secure) {
                issues.push(`${cookie.name}: Not secure (sent over HTTP)`);
            }
            if (!cookie.httpOnly) {
                issues.push(`${cookie.name}: Not httpOnly (accessible via JS)`);
            }
            if (cookie.sameSite === 'none' && !cookie.secure) {
                issues.push(`${cookie.name}: SameSite=None without Secure`);
            }
        }
    }

    if (issues.length > 0) {
        console.warn('Cookie security issues:', issues);
    }
    return issues;
}
```

---

### Security Considerations

1. **Access Control**: Tampermonkey checks @match/@include access to the URL before allowing cookie operations

2. **httpOnly Cookies**: Only available in BETA versions - most session cookies are httpOnly

3. **Secure Flag**: Always set `secure: true` for sensitive cookies

4. **SameSite**: Use `sameSite: 'strict'` or `'lax'` to prevent CSRF

5. **Domain Scope**: Be careful with domain - `.example.com` includes all subdomains

---

## Tampermonkey Tab API Reference

Documentation for tab management and cross-tab communication.

---

### Tab-Persistent Storage

#### GM_getTab(callback)

Get an object that persists for the lifetime of the current tab.

```javascript
// @grant GM_getTab

GM_getTab(function(tab) {
    console.log('Tab object:', tab);

    // Tab object is initially empty {}
    // Add any data you want
    tab.visitCount = (tab.visitCount || 0) + 1;
    tab.lastVisit = Date.now();

    // Data persists across page navigations within this tab
    console.log('Visits in this tab:', tab.visitCount);
});
```

#### GM_saveTab(tab, cb)

Save changes to the tab object.

```javascript
// @grant GM_saveTab

GM_getTab(function(tab) {
    // Modify tab data
    tab.userData = {
        preferences: { theme: 'dark' },
        history: ['page1', 'page2']
    };

    // Save changes
    GM_saveTab(tab, function() {
        console.log('Tab data saved');
    });
});
```

#### GM_getTabs(callback)

Get tab objects from all tabs running the script.

```javascript
// @grant GM_getTabs

GM_getTabs(function(tabs) {
    console.log('All tabs:', tabs);

    // tabs is an object: { tabId1: tabData1, tabId2: tabData2, ... }
    for (const [tabId, tabData] of Object.entries(tabs)) {
        console.log(`Tab ${tabId}:`, tabData);
    }

    // Count active tabs
    const tabCount = Object.keys(tabs).length;
    console.log(`Script running in ${tabCount} tabs`);
});
```

---

### Window Control

#### GM_openInTab(url, options)

Open a new browser tab.

```javascript
// @grant GM_openInTab

// Simple - opens in background
GM_openInTab('https://example.com/');

// Open and focus
GM_openInTab('https://example.com/', { active: true });

// Full options
const newTab = GM_openInTab('https://example.com/', {
    active: true,           // Focus the new tab
    insert: true,           // Insert next to current tab
    setParent: true,        // Current tab is parent (closing parent closes this)
    incognito: false,       // Open in private/incognito mode
    loadInBackground: false // Legacy: opposite of active
});

// Control the opened tab
newTab.onclose = function() {
    console.log('New tab was closed');
};

// Check if closed
if (newTab.closed) {
    console.log('Tab is already closed');
}

// Close programmatically
setTimeout(() => {
    newTab.close();
}, 5000);
```

#### window.close

Close the current tab (requires grant).

```javascript
// @grant window.close

// Close after confirmation
if (confirm('Close this tab?')) {
    window.close();
}

// Note: Cannot close the last tab in a window (security restriction)
```

#### window.focus

Bring the window to the front.

```javascript
// @grant window.focus

// Focus this window/tab
window.focus();

// Unlike unsafeWindow.focus(), this works regardless of browser settings
```

---

### URL Change Detection

#### window.onurlchange

Listen for URL changes in single-page applications (SPAs).

```javascript
// @grant window.onurlchange

// Check if supported
if (window.onurlchange === null) {
    // Feature is supported
    window.addEventListener('urlchange', function(info) {
        console.log('URL changed to:', info.url);

        // Re-run modifications for new page
        if (info.url.includes('/profile')) {
            modifyProfilePage();
        } else if (info.url.includes('/settings')) {
            modifySettingsPage();
        }
    });
}
```

#### Comprehensive SPA Handler

```javascript
// @grant window.onurlchange

(function() {
    'use strict';

    // Initial page load
    handlePage(location.href);

    // URL changes (SPA navigation)
    if (window.onurlchange === null) {
        window.addEventListener('urlchange', (e) => handlePage(e.url));
    }

    function handlePage(url) {
        // Wait for content to load
        setTimeout(() => {
            if (url.includes('/dashboard')) {
                enhanceDashboard();
            } else if (url.includes('/search')) {
                enhanceSearch();
            }
        }, 100);
    }
})();
```

---

### Cross-Tab Communication

#### Using GM_setValue/addValueChangeListener

```javascript
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_addValueChangeListener

// Unique ID for this tab
const TAB_ID = Math.random().toString(36).substr(2, 9);

// Broadcast a message to all tabs
function broadcast(type, data) {
    GM_setValue('broadcast', {
        type: type,
        data: data,
        sender: TAB_ID,
        timestamp: Date.now()
    });
}

// Listen for broadcasts
GM_addValueChangeListener('broadcast', (key, oldVal, newVal, remote) => {
    if (remote && newVal && newVal.sender !== TAB_ID) {
        console.log('Received:', newVal.type, newVal.data);
        handleMessage(newVal.type, newVal.data);
    }
});

function handleMessage(type, data) {
    switch (type) {
        case 'REFRESH':
            location.reload();
            break;
        case 'SETTINGS_CHANGED':
            applySettings(data);
            break;
        case 'PING':
            broadcast('PONG', { respondingTo: data.from });
            break;
    }
}

// Usage
broadcast('SETTINGS_CHANGED', { theme: 'dark' });
```

#### Tab Registry

```javascript
// @grant GM_getTab
// @grant GM_saveTab
// @grant GM_getTabs
// @grant GM_addValueChangeListener

// Register this tab
function registerTab() {
    GM_getTab(tab => {
        tab.id = tab.id || Math.random().toString(36).substr(2, 9);
        tab.registered = Date.now();
        tab.url = location.href;
        GM_saveTab(tab);
    });
}

// Get list of active tabs
function getActiveTabs(callback) {
    GM_getTabs(tabs => {
        const activeTabs = Object.entries(tabs)
            .filter(([id, data]) => data.registered)
            .map(([id, data]) => ({
                id: data.id,
                url: data.url,
                age: Date.now() - data.registered
            }));
        callback(activeTabs);
    });
}

// Check if another tab has the same URL
function isDuplicateTab(callback) {
    GM_getTab(currentTab => {
        GM_getTabs(allTabs => {
            const duplicates = Object.values(allTabs).filter(
                t => t.url === location.href && t.id !== currentTab.id
            );
            callback(duplicates.length > 0, duplicates);
        });
    });
}

// Usage
registerTab();
isDuplicateTab((isDuplicate, others) => {
    if (isDuplicate) {
        console.log('Another tab has this page open:', others);
    }
});
```

#### Leader Election

```javascript
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_addValueChangeListener

const TAB_ID = Math.random().toString(36).substr(2, 9);
let isLeader = false;

async function electLeader() {
    const leader = GM_getValue('leader', null);
    const now = Date.now();

    // Leader is valid if set within last 5 seconds
    if (leader && now - leader.timestamp < 5000 && leader.id !== TAB_ID) {
        isLeader = false;
        return;
    }

    // Claim leadership
    GM_setValue('leader', { id: TAB_ID, timestamp: now });

    // Wait and verify
    await new Promise(r => setTimeout(r, 100));

    const currentLeader = GM_getValue('leader');
    isLeader = currentLeader && currentLeader.id === TAB_ID;

    console.log(isLeader ? 'This tab is the leader' : 'Another tab is leader');
}

// Heartbeat to maintain leadership
setInterval(() => {
    if (isLeader) {
        GM_setValue('leader', { id: TAB_ID, timestamp: Date.now() });
    }
}, 3000);

// Re-elect if leader disappears
GM_addValueChangeListener('leader', () => {
    setTimeout(electLeader, 100);
});

electLeader();

// Only leader performs certain actions
function doLeaderOnlyTask() {
    if (!isLeader) return;
    console.log('Performing leader-only task');
}
```

---

### Async Versions

```javascript
// GM.getTab()
const tab = await GM.getTab();
tab.data = 'value';

// GM.saveTab()
await GM.saveTab(tab);

// GM.getTabs()
const tabs = await GM.getTabs();
```

---

## Tampermonkey Audio API Reference

Documentation for browser tab audio control functions.

---

### Overview

The GM_audio API (v5.0+) allows userscripts to:
- Mute and unmute browser tabs
- Check if a tab is currently playing audio
- Monitor audio state changes

**Required grant:**
```javascript
// @grant GM_audio
```

---

### GM_audio.setMute(details, callback?)

Mute or unmute the current tab.

#### Basic Usage

```javascript
// @grant GM_audio

// Mute the tab
GM_audio.setMute({ isMuted: true }, function(error) {
    if (error) {
        console.error('Failed to mute:', error);
    } else {
        console.log('Tab muted');
    }
});

// Unmute the tab
GM_audio.setMute({ isMuted: false }, function(error) {
    if (error) {
        console.error('Failed to unmute:', error);
    } else {
        console.log('Tab unmuted');
    }
});
```

#### Async Version

```javascript
// @grant GM.audio

// Mute
await GM.audio.setMute({ isMuted: true });
console.log('Tab muted');

// Unmute
await GM.audio.setMute({ isMuted: false });
console.log('Tab unmuted');
```

---

### GM_audio.getState(callback)

Get the current audio state of the tab.

#### Basic Usage

```javascript
// @grant GM_audio

GM_audio.getState(function(state) {
    if (!state) {
        console.error('Failed to get audio state');
        return;
    }

    console.log('Is muted:', state.isMuted);
    console.log('Mute reason:', state.muteReason);  // Why it was muted
    console.log('Is audible:', state.isAudible);    // Currently playing sound
});
```

#### State Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `isMuted` | boolean | Whether tab is currently muted |
| `muteReason` | string | Why the tab was muted (see below) |
| `isAudible` | boolean | Whether tab is currently playing audio |

#### Mute Reasons

| Value | Description |
|-------|-------------|
| `user` | User manually muted (browser UI) |
| `capture` | Muted by tab capture API |
| `extension` | Muted by a browser extension |

#### Async Version

```javascript
// @grant GM.audio

const state = await GM.audio.getState();
console.log(`Muted: ${state.isMuted}, Audible: ${state.isAudible}`);
```

---

### GM_audio.addStateChangeListener(listener, callback)

Listen for changes to the tab's audio state.

#### Basic Usage

```javascript
// @grant GM_audio

function audioListener(event) {
    if ('muted' in event) {
        if (event.muted) {
            console.log('Tab was muted. Reason:', event.muted);
        } else {
            console.log('Tab was unmuted');
        }
    }

    if ('audible' in event) {
        console.log('Audible state changed:', event.audible);
    }
}

GM_audio.addStateChangeListener(audioListener, function(error) {
    if (error) {
        console.error('Failed to add listener:', error);
    } else {
        console.log('Audio state listener registered');
    }
});
```

#### Event Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `muted` | string or false | Mute reason if muted, false if unmuted |
| `audible` | boolean | Current audible state |

#### Async Version

```javascript
// @grant GM.audio

await GM.audio.addStateChangeListener((event) => {
    if (event.muted) {
        console.log('Tab muted by:', event.muted);
    }
    if ('audible' in event) {
        console.log('Audio playing:', event.audible);
    }
});
```

---

### GM_audio.removeStateChangeListener(listener, callback)

Remove a previously registered state change listener.

#### Basic Usage

```javascript
// @grant GM_audio

function myListener(event) {
    console.log('Audio event:', event);
}

// Register
GM_audio.addStateChangeListener(myListener, () => {
    console.log('Listener added');
});

// Later, remove
GM_audio.removeStateChangeListener(myListener, () => {
    console.log('Listener removed');
});
```

#### Async Version

```javascript
// @grant GM.audio

await GM.audio.removeStateChangeListener(myListener);
console.log('Listener removed');
```

---

### Common Patterns

#### Auto-Mute Tab

```javascript
// @grant GM_audio

// Mute tab on script load
GM_audio.setMute({ isMuted: true });

// Or with async
(async () => {
    await GM.audio.setMute({ isMuted: true });
})();
```

#### Mute Toggle with Menu Command

```javascript
// @grant GM_audio
// @grant GM_registerMenuCommand

let isMuted = false;

async function toggleMute() {
    isMuted = !isMuted;
    await GM.audio.setMute({ isMuted });
    console.log(isMuted ? 'Muted' : 'Unmuted');
}

GM_registerMenuCommand('Toggle Mute', toggleMute, 'm');
```

#### Audio Activity Monitor

```javascript
// @grant GM_audio

GM_audio.addStateChangeListener((event) => {
    if ('audible' in event) {
        if (event.audible) {
            console.log('Audio started playing');
            // Maybe show an indicator
            showAudioIndicator(true);
        } else {
            console.log('Audio stopped');
            showAudioIndicator(false);
        }
    }
});

function showAudioIndicator(playing) {
    let indicator = document.getElementById('audio-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'audio-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            background: #333;
            color: white;
            border-radius: 4px;
            z-index: 999999;
        `;
        document.body.appendChild(indicator);
    }
    indicator.textContent = playing ? '🔊 Playing' : '🔇 Silent';
    indicator.style.display = playing ? 'block' : 'none';
}
```

#### Auto-Unmute on Specific Pages

```javascript
// @grant GM_audio

// Unmute when visiting video pages
if (location.pathname.includes('/video/') || location.pathname.includes('/watch')) {
    GM_audio.setMute({ isMuted: false }, (error) => {
        if (!error) {
            console.log('Auto-unmuted for video page');
        }
    });
}
```

#### Remember Mute Preference

```javascript
// @grant GM_audio
// @grant GM_getValue
// @grant GM_setValue

(async () => {
    // Restore user's mute preference
    const wasMuted = GM_getValue('userMutePreference', false);
    await GM.audio.setMute({ isMuted: wasMuted });

    // Listen for changes
    await GM.audio.addStateChangeListener((event) => {
        if ('muted' in event) {
            // Save preference when user changes it
            GM_setValue('userMutePreference', !!event.muted);
        }
    });
})();
```

---

### Error Handling

```javascript
// @grant GM_audio

GM_audio.setMute({ isMuted: true }, (error) => {
    if (error) {
        switch (error) {
            case 'not_supported':
                console.log('Audio control not supported in this browser');
                break;
            case 'permission_denied':
                console.log('Permission to control audio denied');
                break;
            default:
                console.log('Unknown error:', error);
        }
    }
});
```

---

## Tampermonkey DOM and UI API Reference

Documentation for DOM manipulation and UI-related functions.

---

### unsafeWindow

Access the page's actual window object, bypassing the sandbox.

```javascript
// @grant unsafeWindow

// Access page variables
const config = unsafeWindow.pageConfig;
const userData = unsafeWindow.APP.user;

// Call page functions
unsafeWindow.showModal('Hello from userscript!');
unsafeWindow.analytics.track('userscript_loaded');

// Modify page globals
unsafeWindow.DEBUG_MODE = true;
unsafeWindow.featureFlags.newUI = true;

// Listen to page events
unsafeWindow.addEventListener('customEvent', (e) => {
    console.log('Page event:', e.detail);
});
```

#### When to Use unsafeWindow

| Scenario | Use unsafeWindow? |
|----------|-------------------|
| Read page JavaScript variables | Yes |
| Call page-defined functions | Yes |
| Access page's jQuery/React/Vue | Yes |
| DOM manipulation | No (use document) |
| Add event listeners to elements | No |
| Create/modify elements | No |

#### Security Considerations

```javascript
// Safe - reading data
const token = unsafeWindow.authToken;

// Dangerous - executing untrusted code
// unsafeWindow.eval(userInput);  // DON'T DO THIS

// Be careful with callbacks
unsafeWindow.someFunction({
    callback: function() {
        // This runs in page context - be careful!
    }
});
```

---

### GM_addStyle(css)

Add CSS styles to the document. Useful for customising page appearance.

```javascript
// @grant GM_addStyle

// Basic styling
GM_addStyle(`
    .my-class {
        background: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }
`);

// Hide elements
GM_addStyle(`
    #annoying-banner,
    .popup-overlay,
    .cookie-notice {
        display: none !important;
    }
`);

// Dark mode
GM_addStyle(`
    body {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }

    a {
        color: #6db3f2 !important;
    }

    img {
        filter: brightness(0.9);
    }
`);

// Returns the style element
const styleEl = GM_addStyle('body { font-size: 16px; }');
console.log('Style element:', styleEl);
```

#### Dynamic Styles

```javascript
// Toggle styles
let darkModeStyle = null;

function toggleDarkMode() {
    if (darkModeStyle) {
        darkModeStyle.remove();
        darkModeStyle = null;
    } else {
        darkModeStyle = GM_addStyle(`
            body { background: #1a1a1a; color: #fff; }
        `);
    }
}

GM_registerMenuCommand('Toggle Dark Mode', toggleDarkMode);
```

---

### GM_addElement(tag_name, attributes)
### GM_addElement(parent_node, tag_name, attributes)

Create and inject HTML elements. Can bypass Content Security Policy (CSP).

#### Add Script

```javascript
// @grant GM_addElement

// Inline script
GM_addElement('script', {
    textContent: `
        window.myGlobal = 'injected';
        console.log('Script injected!');
    `
});

// External script
GM_addElement('script', {
    src: 'https://example.com/library.js',
    type: 'text/javascript'
});

// Module script
GM_addElement('script', {
    src: 'https://example.com/module.mjs',
    type: 'module'
});
```

#### Add Styles

```javascript
// Inline styles
GM_addElement('style', {
    textContent: `
        body { font-family: Arial; }
        .highlight { background: yellow; }
    `
});

// External stylesheet
GM_addElement('link', {
    rel: 'stylesheet',
    href: 'https://example.com/style.css'
});
```

#### Add to Specific Parent

```javascript
// Add to body
GM_addElement(document.body, 'div', {
    id: 'my-container',
    className: 'userscript-ui'
});

// Add to specific element
const container = document.querySelector('#main');
GM_addElement(container, 'button', {
    textContent: 'Click Me',
    onclick: () => alert('Clicked!')
});

// Add to Shadow DOM
const shadowRoot = element.shadowRoot;
GM_addElement(shadowRoot, 'style', {
    textContent: 'div { color: blue; }'
});
```

#### Add Images

```javascript
GM_addElement('img', {
    src: 'https://example.com/image.png',
    alt: 'Description',
    width: 100,
    height: 100,
    style: 'border-radius: 50%;'
});
```

#### Bypassing CSP

```javascript
// Sites with strict CSP block inline scripts
// GM_addElement can bypass this

// Instead of (may be blocked by CSP):
const script = document.createElement('script');
script.textContent = 'console.log("blocked")';
document.head.appendChild(script);

// Use (bypasses CSP):
GM_addElement('script', {
    textContent: 'console.log("works!")'
});
```

---

### Creating Custom UI

#### Floating Panel

```javascript
function createPanel() {
    const panel = document.createElement('div');
    panel.id = 'userscript-panel';
    panel.innerHTML = `
        <div class="panel-header">
            <span>My Script</span>
            <button class="close-btn">&times;</button>
        </div>
        <div class="panel-content">
            <label>
                <input type="checkbox" id="feature1"> Enable Feature 1
            </label>
            <label>
                <input type="checkbox" id="feature2"> Enable Feature 2
            </label>
        </div>
    `;

    document.body.appendChild(panel);

    // Add styles
    GM_addStyle(`
        #userscript-panel {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 250px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 999999;
            font-family: system-ui, sans-serif;
        }

        #userscript-panel .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            background: #f5f5f5;
            border-radius: 8px 8px 0 0;
            border-bottom: 1px solid #e0e0e0;
        }

        #userscript-panel .close-btn {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #666;
        }

        #userscript-panel .panel-content {
            padding: 15px;
        }

        #userscript-panel label {
            display: block;
            margin-bottom: 10px;
            cursor: pointer;
        }
    `);

    // Event handlers
    panel.querySelector('.close-btn').onclick = () => panel.remove();

    return panel;
}

GM_registerMenuCommand('Open Panel', createPanel);
```

#### Toast Notifications

```javascript
function showToast(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'userscript-toast';
    toast.textContent = message;
    document.body.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto-remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

GM_addStyle(`
    .userscript-toast {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background: #333;
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        z-index: 999999;
        opacity: 0;
        transition: all 0.3s ease;
    }

    .userscript-toast.show {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
`);

// Usage
showToast('Settings saved!');
```

#### Draggable Element

```javascript
function makeDraggable(element) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    const header = element.querySelector('.panel-header') || element;
    header.style.cursor = 'move';

    header.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        element.style.top = (element.offsetTop - pos2) + 'px';
        element.style.left = (element.offsetLeft - pos1) + 'px';
        element.style.right = 'auto';
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

// Usage
const panel = createPanel();
makeDraggable(panel);
```

---

### Interacting with Page Frameworks

#### Inject into React App

```javascript
// @grant unsafeWindow

// Wait for React
function waitForReact(callback) {
    const interval = setInterval(() => {
        if (unsafeWindow.React && unsafeWindow.ReactDOM) {
            clearInterval(interval);
            callback(unsafeWindow.React, unsafeWindow.ReactDOM);
        }
    }, 100);
}

// Access React component state
function getReactState(element) {
    const key = Object.keys(element).find(k => k.startsWith('__reactInternalInstance'));
    if (key) {
        let fiber = element[key];
        while (fiber) {
            if (fiber.memoizedState) return fiber.memoizedState;
            fiber = fiber.return;
        }
    }
    return null;
}
```

#### Inject into Vue App

```javascript
// @grant unsafeWindow

// Access Vue component
const vueElement = document.querySelector('#app');
const vueInstance = vueElement.__vue__;

if (vueInstance) {
    console.log('Vue data:', vueInstance.$data);
    // Modify Vue state
    vueInstance.someProperty = 'new value';
}
```

#### Inject into Angular App

```javascript
// @grant unsafeWindow

// Access Angular scope (AngularJS)
const element = document.querySelector('[ng-controller]');
const scope = unsafeWindow.angular.element(element).scope();

if (scope) {
    scope.$apply(() => {
        scope.someValue = 'modified';
    });
}
```

---

## HTTP Requests API Reference

Documentation for GM_xmlhttpRequest - cross-origin HTTP requests.

---

### Overview

GM_xmlhttpRequest allows userscripts to make HTTP requests to any domain, bypassing the browser's same-origin policy. This is one of the most powerful Tampermonkey APIs.

---

### Required Setup

```javascript
// @grant GM_xmlhttpRequest
// @connect api.example.com
// @connect *.googleapis.com
```

**Important:** Always declare domains with `@connect`. Without it, users get permission dialogs or requests fail.

---

### Basic Examples

#### GET Request

```javascript
GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.example.com/data',
    onload: function(response) {
        console.log('Status:', response.status);
        console.log('Response:', response.responseText);
    },
    onerror: function(error) {
        console.error('Request failed');
    }
});
```

#### POST Request with JSON

```javascript
GM_xmlhttpRequest({
    method: 'POST',
    url: 'https://api.example.com/submit',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    data: JSON.stringify({
        name: 'John',
        email: 'john@example.com'
    }),
    onload: function(response) {
        const result = JSON.parse(response.responseText);
        console.log('Success:', result);
    }
});
```

---

### Full Options Reference

```javascript
GM_xmlhttpRequest({
    // Request configuration
    method: 'POST',                    // GET, HEAD, POST, PUT, DELETE, PATCH
    url: 'https://api.example.com/',   // Target URL (or Blob/File v5.4.6226+)
    headers: {                         // Custom headers
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token123',
        'X-Custom-Header': 'value'
    },
    data: 'request body',              // String, Blob, File, FormData, URLSearchParams, ArrayBuffer, UInt8Array (v5.4+)

    // Request modifiers
    timeout: 30000,                    // Timeout in milliseconds
    binary: false,                     // Send data in binary mode
    nocache: false,                    // Don't cache the resource
    revalidate: false,                 // Revalidate cached content
    anonymous: false,                  // Don't send cookies (enforces fetch mode)
    fetch: false,                      // Use fetch instead of XMLHttpRequest

    // Authentication
    user: 'username',                  // Basic auth username
    password: 'password',              // Basic auth password
    cookie: 'name=value',              // Cookie to include
    cookiePartition: {                 // Partitioned cookies (v5.2+)
        topLevelSite: 'https://example.com'
    },

    // Response handling
    responseType: 'json',              // arraybuffer, blob, json, stream
    overrideMimeType: 'text/plain',    // Override response MIME type

    // Redirect handling (v6180+)
    redirect: 'follow',                // follow, error, manual

    // Context for callbacks
    context: { custom: 'data' },       // Passed to response object

    // Proxy (Firefox only v5.5.6233+)
    proxy: {
        type: 'http',                  // direct, http, https, socks, socks4
        host: 'proxy.example.com',
        port: 8080,
        username: 'proxyuser',
        password: 'proxypass',
        proxyDNS: true,
        failoverTimeout: 5,
        proxyAuthorizationHeader: 'Basic ...',
        connectionIsolationKey: 'key'
    },

    // Callbacks
    onload: function(response) {},
    onerror: function(response) {},
    onabort: function(response) {},
    ontimeout: function(response) {},
    onprogress: function(progress) {},
    onreadystatechange: function(response) {},
    onloadstart: function(response) {}  // For stream responseType
});
```

---

### Response Object

```javascript
onload: function(response) {
    response.finalUrl;        // Final URL after redirects
    response.readyState;      // XMLHttpRequest readyState (4 = DONE)
    response.status;          // HTTP status code (200, 404, etc.)
    response.statusText;      // HTTP status text ("OK", "Not Found")
    response.responseHeaders; // Response headers as string
    response.response;        // Parsed response (if responseType set)
    response.responseText;    // Raw response text
    response.responseXML;     // Parsed XML (if applicable)
    response.context;         // Custom context from request
}
```

---

### @connect Directive

Whitelist domains for GM_xmlhttpRequest.

```javascript
// Specific domain (includes subdomains)
// @connect api.example.com

// Subdomain pattern
// @connect *.googleapis.com

// Current page's domain
// @connect self

// Localhost
// @connect localhost
// @connect 127.0.0.1

// Any IP address
// @connect 192.168.1.1

// Allow all (prompts user)
// @connect *
```

**Best practice:**
1. Declare all known domains explicitly
2. Add `@connect *` as fallback for "allow all" option
3. Both initial URL and final URL (after redirects) are checked

---

### Advanced Features

#### Aborting Requests

```javascript
const request = GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.example.com/large-file',
    onload: response => console.log('Done'),
    onabort: () => console.log('Aborted')
});

// Cancel after 5 seconds
setTimeout(() => request.abort(), 5000);
```

#### Progress Tracking

```javascript
GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://example.com/large-file.zip',
    onprogress: function(progress) {
        if (progress.lengthComputable) {
            const percent = (progress.loaded / progress.total * 100).toFixed(2);
            console.log(`Downloaded: ${percent}%`);
        }
    },
    onload: response => console.log('Complete')
});
```

#### Streaming Response

```javascript
GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.example.com/stream',
    responseType: 'stream',
    onloadstart: function(response) {
        const reader = response.response.getReader();

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) return;
                console.log('Chunk:', new TextDecoder().decode(value));
                read();
            });
        }

        read();
    }
});
```

---

### Common Patterns

#### REST API Client

```javascript
// @grant GM_xmlhttpRequest
// @connect api.example.com

const api = {
    baseUrl: 'https://api.example.com',
    token: null,

    request(method, endpoint, data = null) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                method: method,
                url: this.baseUrl + endpoint,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': this.token ? `Bearer ${this.token}` : ''
                },
                data: data ? JSON.stringify(data) : null,
                onload: response => {
                    if (response.status >= 200 && response.status < 300) {
                        resolve(JSON.parse(response.responseText));
                    } else {
                        reject(new Error(`HTTP ${response.status}`));
                    }
                },
                onerror: reject
            });
        });
    },

    get(endpoint) { return this.request('GET', endpoint); },
    post(endpoint, data) { return this.request('POST', endpoint, data); },
    put(endpoint, data) { return this.request('PUT', endpoint, data); },
    delete(endpoint) { return this.request('DELETE', endpoint); }
};

// Usage
api.token = 'your-api-token';
api.get('/users/123').then(user => console.log(user));
```

#### Form Data Upload

```javascript
const formData = new FormData();
formData.append('file', blob, 'filename.txt');
formData.append('description', 'My file');

GM_xmlhttpRequest({
    method: 'POST',
    url: 'https://api.example.com/upload',
    data: formData,
    onload: response => console.log('Uploaded!')
});
```

#### Binary Data Upload (v5.4+)

ArrayBuffer and UInt8Array can be sent directly as the request body:

```javascript
// Send raw binary data
const buffer = new ArrayBuffer(256);
const view = new Uint8Array(buffer);
// ... populate buffer ...

GM_xmlhttpRequest({
    method: 'POST',
    url: 'https://api.example.com/binary',
    headers: { 'Content-Type': 'application/octet-stream' },
    data: buffer,   // ArrayBuffer or UInt8Array
    onload: response => console.log('Binary sent!')
});
```

#### Retry with Exponential Backoff

```javascript
function requestWithRetry(options, maxRetries = 3) {
    return new Promise((resolve, reject) => {
        let attempt = 0;

        function tryRequest() {
            GM_xmlhttpRequest({
                ...options,
                onload: resolve,
                onerror: (error) => {
                    if (++attempt < maxRetries) {
                        const delay = Math.pow(2, attempt) * 1000;
                        console.log(`Retry ${attempt} in ${delay}ms`);
                        setTimeout(tryRequest, delay);
                    } else {
                        reject(error);
                    }
                }
            });
        }

        tryRequest();
    });
}
```

#### Handle Different Response Types

```javascript
// JSON response
GM_xmlhttpRequest({
    url: 'https://api.example.com/data.json',
    responseType: 'json',
    onload: r => console.log(r.response)  // Already parsed
});

// Binary data
GM_xmlhttpRequest({
    url: 'https://example.com/image.png',
    responseType: 'blob',
    onload: response => {
        const url = URL.createObjectURL(response.response);
        img.src = url;
    }
});

// ArrayBuffer
GM_xmlhttpRequest({
    url: 'https://example.com/data.bin',
    responseType: 'arraybuffer',
    onload: response => {
        const view = new DataView(response.response);
        console.log(view.getUint32(0));
    }
});
```

---

### Async/Await Version

Use GM.xmlHttpRequest (note uppercase H) for promises:

```javascript
// @grant GM.xmlHttpRequest
// @connect api.example.com

try {
    const response = await GM.xmlHttpRequest({
        method: 'GET',
        url: 'https://api.example.com/data'
    });
    const data = JSON.parse(response.responseText);
    console.log(data);
} catch (error) {
    console.error('Request failed:', error);
}
```

The promise also has an `abort()` function:

```javascript
const request = GM.xmlHttpRequest({
    method: 'GET',
    url: 'https://api.example.com/large-file'
});

// Cancel after 5 seconds
setTimeout(() => request.abort(), 5000);

try {
    const response = await request;
} catch (error) {
    console.log('Request was aborted or failed');
}
```

---

### Error Handling

Always include error handlers:

```javascript
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (response) => {
        if (response.status >= 200 && response.status < 300) {
            try {
                const data = JSON.parse(response.responseText);
                processData(data);
            } catch (e) {
                console.error('Invalid JSON:', e);
            }
        } else {
            console.error('HTTP error:', response.status, response.statusText);
        }
    },
    onerror: (error) => {
        console.error('Network error:', error);
    },
    ontimeout: () => {
        console.error('Request timed out');
    }
});
```

---

## Web Request Interception API Reference

Documentation for GM_webRequest - intercept and modify browser requests.

---

### Overview

GM_webRequest allows userscripts to intercept, block, or redirect web requests before they're made. This is useful for:
- Blocking ads and tracking
- Redirecting URLs
- Modifying request patterns

**Important Limitations:**
- **Experimental API** - may change at any time
- **Not available in Manifest V3** (Chrome 5.2+, Edge)
- **Firefox only** for current usage
- Only handles: `sub_frame`, `script`, `xhr`, `websocket` request types

---

### Required Setup

```javascript
// @grant GM_webRequest
```

---

### Basic Usage

```javascript
GM_webRequest([
    // Cancel requests to ads
    {
        selector: '*://ads.example.com/*',
        action: 'cancel'
    },

    // Redirect tracking URLs
    {
        selector: '*://tracker.example.com/*',
        action: {
            redirect: 'https://example.com/blocked'
        }
    },

    // Pattern-based redirect
    {
        selector: { match: '*://old.example.com/*' },
        action: {
            redirect: {
                from: '([^:]+)://old.example.com/(.*)',
                to: '$1://new.example.com/$2'
            }
        }
    },

    // Exclude certain paths
    {
        selector: {
            include: '*://example.com/*',
            exclude: '*://example.com/api/*'
        },
        action: 'cancel'
    }
], function(info, message, details) {
    console.log('Action:', info);        // 'cancel' or 'redirect'
    console.log('Message:', message);    // 'ok' or 'error'
    console.log('URL:', details.url);
    console.log('Redirect URL:', details.redirect_url);
});
```

---

### Rule Properties

#### Selector

Defines which URLs the rule matches.

| Property | Type | Description |
|----------|------|-------------|
| `selector` | string | Simple URL pattern |
| `selector.include` | string/array | URLs to include |
| `selector.match` | string/array | Match patterns |
| `selector.exclude` | string/array | URLs to exclude |

```javascript
// String selector (simplest)
{ selector: '*://ads.example.com/*' }

// Object selector with include/exclude
{
    selector: {
        include: '*://example.com/*',
        exclude: '*://example.com/api/*'
    }
}

// Array of patterns
{
    selector: {
        include: ['*://ads1.com/*', '*://ads2.com/*'],
        match: '*://tracker.com/*'
    }
}
```

#### Action

Defines what to do when a URL matches.

| Property | Type | Description |
|----------|------|-------------|
| `action` | string | `'cancel'` to block |
| `action.cancel` | boolean | Block the request |
| `action.redirect` | string/object | Redirect destination |

```javascript
// Cancel (block) the request
{ action: 'cancel' }
{ action: { cancel: true } }

// Redirect to static URL
{ action: { redirect: 'https://example.com/blocked' } }

// Redirect with pattern replacement
{
    action: {
        redirect: {
            from: '([^:]+)://old.com/(.*)',
            to: '$1://new.com/$2'
        }
    }
}
```

---

### @webRequest Header

Define rules at script level (applies before script loads):

```javascript
// @webRequest {"selector": "*://ads.example.com/*", "action": "cancel"}
// @webRequest {"selector": {"include": "*tracking*"}, "action": {"redirect": "about:blank"}}
```

This is useful for blocking resources that load before your script runs.

---

### Listener Callback

```javascript
GM_webRequest(rules, function(info, message, details) {
    // info: 'cancel' or 'redirect'
    // message: 'ok' or 'error'
    // details: {
    //     rule: <the triggered rule>,
    //     url: <request URL>,
    //     redirect_url: <where redirected>,
    //     description: <error description if any>
    // }
});
```

---

### Common Use Cases

#### Block Ads

```javascript
GM_webRequest([
    { selector: '*://ads.example.com/*', action: 'cancel' },
    { selector: '*://tracking.example.com/*', action: 'cancel' },
    { selector: '*://analytics.example.com/*', action: 'cancel' }
]);
```

#### Redirect Old URLs

```javascript
GM_webRequest([
    {
        selector: { match: '*://old-domain.com/*' },
        action: {
            redirect: {
                from: '([^:]+)://old-domain.com/(.*)',
                to: '$1://new-domain.com/$2'
            }
        }
    }
]);
```

#### Block Specific Resource Types

```javascript
// Block scripts from untrusted domains
GM_webRequest([
    {
        selector: {
            include: '*://*.untrusted.com/*.js'
        },
        action: 'cancel'
    }
]);
```

#### Redirect to Local Resources

```javascript
GM_webRequest([
    {
        selector: 'https://cdn.example.com/library.js',
        action: {
            redirect: 'https://my-cdn.com/modified-library.js'
        }
    }
]);
```

---

### Limitations

#### Browser Support

| Browser | GM_webRequest Support |
|---------|----------------------|
| Firefox | ✅ Supported |
| Chrome (MV3) | ❌ Not available |
| Edge (MV3) | ❌ Not available |
| Safari | ❌ Not available |

#### Request Types

Only these request types can be intercepted:
- `sub_frame` - iframes
- `script` - JavaScript files
- `xhr` - XMLHttpRequest/fetch
- `websocket` - WebSocket connections

These **cannot** be intercepted:
- Main document (`main_frame`)
- Images
- Stylesheets
- Fonts

---

### Alternatives for MV3

Since GM_webRequest doesn't work in Chrome/Edge MV3, use these alternatives:

#### Page-Level Interception

```javascript
// @grant unsafeWindow

// Intercept fetch
const originalFetch = unsafeWindow.fetch;
unsafeWindow.fetch = function(...args) {
    const url = args[0]?.url || args[0];
    console.log('Intercepted fetch:', url);

    // Block certain URLs
    if (url.includes('tracking.com')) {
        return Promise.reject(new Error('Blocked'));
    }

    return originalFetch.apply(this, args);
};

// Intercept XMLHttpRequest
const originalOpen = unsafeWindow.XMLHttpRequest.prototype.open;
unsafeWindow.XMLHttpRequest.prototype.open = function(method, url) {
    console.log('Intercepted XHR:', method, url);

    // Block certain URLs
    if (url.includes('tracking.com')) {
        throw new Error('Blocked');
    }

    return originalOpen.apply(this, arguments);
};
```

#### Remove Elements After Load

```javascript
// Remove ad iframes after they load
const observer = new MutationObserver(() => {
    document.querySelectorAll('iframe[src*="ads"]').forEach(el => el.remove());
});
observer.observe(document.body, { childList: true, subtree: true });
```

#### Use CSS to Hide

```javascript
// @grant GM_addStyle

GM_addStyle(`
    iframe[src*="ads"],
    [id*="advertisement"],
    [class*="sponsored"] {
        display: none !important;
    }
`);
```

---

### Best Practices

1. **Be specific with selectors** - Avoid overly broad patterns
2. **Test thoroughly** - Request interception can break sites
3. **Provide fallbacks** - Check if GM_webRequest is available
4. **Log actions** - Use the listener callback for debugging
5. **Consider MV3 alternatives** - Your script may need to work in Chrome too

```javascript
// Check if GM_webRequest is available
if (typeof GM_webRequest !== 'undefined') {
    GM_webRequest([...rules...]);
} else {
    console.log('GM_webRequest not available, using fallback');
    // Use page-level interception instead
}
```

---

## ScriptCat 特有 API 参考

以下 API 和元数据为 ScriptCat 独有，不兼容 Tampermonkey / Violentmonkey。使用时建议在注释中标注 `// ScriptCat only`。

---

### 后台脚本与定时任务

#### @background

声明脚本为后台脚本，在 Service Worker 中运行，无需匹配页面。

```js
// ==UserScript==
// @name         后台监控脚本
// @background
// @grant        GM_xmlhttpRequest
// @grant        GM_notification
// @connect      api.example.com
// ==/UserScript==

const resp = await GM.xmlHttpRequest({
  url: "https://api.example.com/status",
});
const data = JSON.parse(resp.responseText);
if (data.hasUpdate) {
  GM.notification({ title: "有新更新", text: data.message });
}
```

**注意**：后台脚本无法访问 DOM（没有 document/window），只能使用 GM API。

#### @crontab

定时执行表达式，配合 `@background` 使用。格式为 6 位 cron：`秒 分 时 日 月 周`。

```js
// @background
// @crontab      0 0 9 * * *        // 每天 9:00:00
// @crontab      0 */30 * * * *     // 每 30 分钟
// @crontab      0 0 9 * * 1-5      // 工作日 9:00
// @crontab      0 0 8,12,18 * * *  // 每天 8:00、12:00、18:00
// @crontab      once 2025-12-31 00:00:00  // 一次性，指定时间
```

每次触发时脚本重新执行。脚本执行完毕后自动回收。

#### CATRetryError

在后台脚本中抛出此错误可让 ScriptCat 稍后重试。

```js
// @background
try {
  const resp = await GM.xmlHttpRequest({ url: "https://api.example.com/data" });
  if (resp.status === 429) {
    throw new CATRetryError("请求限流", 60); // 60 秒后重试
  }
  // 处理数据...
} catch (e) {
  if (e instanceof CATRetryError) throw e;
  throw new CATRetryError("请求失败，稍后重试", 300); // 5 分钟后重试
}
```

构造函数：
- `new CATRetryError(message, seconds)` — N 秒后重试
- `new CATRetryError(message, date)` — 指定时间重试

最小重试间隔 5 秒。

---

### ScriptCat 独有函数

#### CAT_registerMenuInput

注册带输入框的菜单项。用户点击后弹出输入对话框。

```js
// @grant GM_registerMenuCommand  // 共用同一个 grant

CAT_registerMenuInput("设置延迟时间", (value) => {
  console.log("用户输入:", value);
}, {
  inputType: "number",       // "text" | "number" | "boolean"
  title: "延迟设置",
  inputLabel: "延迟秒数",
  inputDefaultValue: 5,
  inputPlaceholder: "请输入秒数",
});

// 取消注册
CAT_unregisterMenuInput(menuId);
```

#### CAT_userConfig

打开脚本的用户配置页面（需在元数据中定义 UserConfig）。

```js
// @grant GM_registerMenuCommand

GM_registerMenuCommand("打开设置", () => {
  CAT_userConfig();
});
```

#### CAT_fetchDocument

获取 URL 内容并解析为 Document 对象。在内容脚本上下文中可用。

```js
const doc = await CAT_fetchDocument("https://example.com/page");
if (doc) {
  const title = doc.querySelector("title")?.textContent;
  const links = doc.querySelectorAll("a");
}
```

#### CAT_createBlobUrl

从 Blob 创建 URL。ScriptCat 管理 URL 生命周期（自动回收）。

```js
const blob = new Blob(["Hello"], { type: "text/plain" });
const url = await CAT_createBlobUrl(blob);
// 可在页面 DOM 中使用此 URL
```

#### CAT_fetchBlob

获取 URL 内容作为 Blob。主要用于 `GM.xmlHttpRequest` 的 stream 响应。

```js
const blob = await CAT_fetchBlob("blob:chrome-extension://xxx/yyy");
```

#### CAT_scriptLoaded

配合 `@early-start` 使用。通知 ScriptCat 脚本已完成初始化。

```js
// @early-start

// 脚本极早执行，可以拦截全局对象
Object.defineProperty(window, 'someGlobal', { value: 'intercepted' });

// 通知初始化完成
await CAT_scriptLoaded();
```

---

### 文件存储

#### CAT_fileStorage

操作 ScriptCat 的云端/本地文件存储系统。每个脚本有独立的 `app/<uuid>` 目录。

```js
// 上传文件
CAT_fileStorage("upload", {
  path: "data/export.json",
  data: new Blob([JSON.stringify(data)], { type: "application/json" }),
  onload: () => console.log("上传成功"),
  onerror: (err) => console.error("上传失败:", err.error),
});

// 列出文件
CAT_fileStorage("list", {
  path: "data/",
  onload: (files) => {
    // files: [{ name, path, absPath, size, digest, createtime, updatetime }]
    files.forEach(f => console.log(f.name, f.size));
  },
});

// 下载文件
CAT_fileStorage("download", {
  file: fileInfo, // 从 list 返回的文件对象
  onload: (blob) => {
    const text = await blob.text();
  },
});

// 删除文件
CAT_fileStorage("delete", {
  path: "data/old.json",
  onload: () => console.log("删除成功"),
});

// 打开存储配置
CAT_fileStorage("config");
```

**错误码**：
| code | 含义 |
|------|------|
| 1 | 存储未配置 |
| 2 | 配置错误 |
| 3 | 路径不存在 |
| 4 | 上传失败 |
| 5 | 下载失败 |
| 6 | 删除失败 |
| 7 | 文件路径不允许 |
| 8 | 网络错误 |

---

### GM_registerMenuCommand 扩展选项

ScriptCat 对标准 `GM_registerMenuCommand` 增加了以下选项：

```js
GM_registerMenuCommand("菜单项", callback, {
  accessKey: "m",
  autoClose: true,
  nested: false,      // SC: false 时提升到浏览器右键菜单
  individual: true,   // SC: 不合并同名菜单项
});

// GM.registerMenuCommand 额外支持：
await GM.registerMenuCommand("菜单项", callback, {
  icon: "https://example.com/icon.png", // SC: 菜单图标
  closeOnClick: true,                    // SC: alias for autoClose
});
```

---

### CAT.agent.* — Agent API

ScriptCat Agent 扩展 API，用于在用户脚本中调用 AI 能力和浏览器自动化。每个子 API 需单独声明 `@grant`。

#### CAT.agent.conversation — AI 对话

创建 LLM 对话，支持工具调用和流式输出。

```js
// @grant CAT.agent.conversation

const conv = await CAT.agent.conversation.create({
  system: "你是一个翻译助手",
  model: "model-id",       // 可选，默认使用用户配置的模型
  maxIterations: 10,
  tools: [{
    name: "get_page_text",
    description: "获取当前页面文本",
    parameters: { type: "object", properties: {} },
    handler: async () => document.body.innerText.slice(0, 5000),
  }],
});

// 非流式
const reply = await conv.chat("翻译这段话：Hello World");
console.log(reply.content);

// 流式
const stream = await conv.chatStream("翻译页面内容");
for await (const chunk of stream) {
  if (chunk.type === "content_delta") process.stdout.write(chunk.content);
  if (chunk.type === "tool_call") console.log("调用工具:", chunk.toolCall.name);
  if (chunk.type === "error") console.error(chunk.error);
}
```

#### CAT.agent.dom — 浏览器 DOM 操作

```js
// @grant CAT.agent.dom

const tabs = await CAT.agent.dom.listTabs();
await CAT.agent.dom.navigate("https://example.com", { tabId: tabs[0].tabId });
const page = await CAT.agent.dom.readPage({ tabId: tabs[0].tabId, selector: "main" });
const screenshot = await CAT.agent.dom.screenshot({ tabId: tabs[0].tabId });
await CAT.agent.dom.click("#button", { tabId: tabs[0].tabId, trusted: true });
await CAT.agent.dom.fill("input[name=q]", "text", { tabId: tabs[0].tabId });
await CAT.agent.dom.scroll("down", { tabId: tabs[0].tabId });
await CAT.agent.dom.waitFor(".result", { tabId: tabs[0].tabId, timeout: 5000 });
const result = await CAT.agent.dom.executeScript("return document.title", { tabId: tabs[0].tabId });
```

#### CAT.agent.task — 定时任务管理

```js
// @grant CAT.agent.task

// 创建定时任务（Agent 自动执行 prompt）
const task = await CAT.agent.task.create({
  name: "每日检查",
  crontab: "0 9 * * *",
  mode: "internal",
  enabled: true,
  prompt: "检查仪表盘并汇总异常",
  skills: "auto",
});

// 创建事件模式任务（脚本自己处理）
const eventTask = await CAT.agent.task.create({
  name: "数据同步",
  crontab: "0 */30 * * *",
  mode: "event",
  enabled: true,
});
CAT.agent.task.addListener(eventTask.id, (trigger) => {
  console.log("触发:", trigger.name, trigger.triggeredAt);
});
```

#### CAT.agent.skills — Skill 管理

```js
// @grant CAT.agent.skills

const skills = await CAT.agent.skills.list();
const result = await CAT.agent.skills.call("browser-automation", "screenshot", { tabId: 123 });
```

#### CAT.agent.model — 模型查询

```js
// @grant CAT.agent.model

const models = await CAT.agent.model.list();
const defaultId = await CAT.agent.model.getDefault();
```

#### CAT.agent.opfs — 工作区文件系统

```js
// @grant CAT.agent.opfs

await CAT.agent.opfs.write("data/report.txt", "内容...");
const file = await CAT.agent.opfs.read("data/report.txt");
const entries = await CAT.agent.opfs.list("data/");
await CAT.agent.opfs.delete("data/old.txt");
```

---

### 完整后台脚本示例

```js
// ==UserScript==
// @name         价格监控
// @namespace    https://scriptcat.org/
// @version      0.1.0
// @description  每小时检查商品价格，降价时通知 // ScriptCat only
// @background
// @crontab      0 0 * * * *
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_notification
// @connect      api.example.com
// ==/UserScript==

"use strict";

const TARGET_URL = "https://api.example.com/product/123";
const PRICE_KEY = "last_price";

try {
  const resp = await GM.xmlHttpRequest({ url: TARGET_URL, responseType: "json" });
  const currentPrice = resp.response.price;
  const lastPrice = await GM.getValue(PRICE_KEY, Infinity);

  if (currentPrice < lastPrice) {
    GM.notification({
      title: "降价提醒！",
      text: `价格从 ¥${lastPrice} 降到 ¥${currentPrice}`,
      timeout: 0, // 不自动消失
    });
  }

  await GM.setValue(PRICE_KEY, currentPrice);
} catch (e) {
  throw new CATRetryError("检查失败，5 分钟后重试", 300);
}
```

---

---
name: scriptcat-dev
description: 脚本猫/油猴脚本开发助手 — 帮助编写、调试和优化 UserScript 用户脚本。覆盖标准 GM API（兼容 Tampermonkey/Violentmonkey）和 ScriptCat 特有功能（后台脚本、定时任务、Agent API、文件存储）。当用户想写油猴脚本、用户脚本、ScriptCat 脚本或者需要对网页进行自动化修改时使用。
scripts:
  - analyze_page.js
references:
  - gm_api.md
  - metadata.md
  - patterns.md
  - scriptcat_api.md
---

## 用户脚本开发助手

你现在可以帮助用户编写 ScriptCat / Tampermonkey 用户脚本（.user.js）。你掌握完整的 UserScript API 知识，可以按需加载详细参考文档。

### 可用资源

| 类型 | 名称 | Input → Output / 何时加载 |
|------|------|--------------------------|
| 脚本 | `analyze_page` | tabId → { framework, selectors[], dynamicElements[], globals[] } |
| 参考 | `metadata` | 写元数据块时不确定字段 → `read_reference("scriptcat-dev", "metadata")` |
| 参考 | `gm_api` | 需要 GM API 用法 → `read_reference("scriptcat-dev", "gm_api")` |
| 参考 | `scriptcat_api` | 需要 ScriptCat 特有功能 → `read_reference("scriptcat-dev", "scriptcat_api")` |
| 参考 | `patterns` | 需要常见模式参考 → `read_reference("scriptcat-dev", "patterns")` |

### 工作流

#### 从零开发新脚本

1. **需求澄清**：`ask_user` 确认目标网站、功能需求、是否需要 ScriptCat 特有功能
2. **页面分析**（可选）：如果用户已打开目标网站，用 `analyze_page` 分析页面结构，获取选择器和框架信息
3. **加载参考**：按需 `read_reference` 加载需要的 API 文档
4. **生成脚本**：
   - 先写 `==UserScript==` 元数据块（不确定字段用法时查 `metadata` 参考）
   - 按最小权限原则声明 `@grant`
   - 编写功能代码
5. **交付**：展示完整脚本，说明关键实现和安装方式

#### 修改/优化现有脚本

1. 阅读用户提供的脚本代码，分析结构
2. 指出问题并提出改进（性能、安全、兼容性）
3. 输出修改后的完整脚本

#### 调试脚本

1. 分析用户描述的问题 + 脚本代码
2. 对照「常见问题排查」表检查
3. 给出修复方案和解释

#### ScriptCat 高级功能

当用户需要后台脚本、定时任务、Agent API 集成时，`read_reference("scriptcat-dev", "scriptcat_api")` 加载参考。

### 脚本模板

```js
// ==UserScript==
// @name         脚本名称
// @namespace    https://scriptcat.org/
// @version      0.1.0
// @description  脚本描述
// @author       作者
// @match        https://example.com/*
// @grant        none
// ==/UserScript==

"use strict";

// 代码从这里开始
```

### 编码规范

#### @match 模式

- `*://*.example.com/*` — 匹配 http/https 所有子域
- `https://example.com/path/*` — 精确路径前缀
- 避免 `*://*/*` — 过于宽泛，影响性能和安全

#### @grant 最小权限

- 不需要 GM API 时用 `@grant none`
- `@grant none` 时脚本在页面作用域运行，可直接访问页面变量
- 声明任何 `@grant` 后脚本运行在沙箱中，需用 `unsafeWindow` 访问页面变量
- 每个用到的 GM API 都必须单独声明

#### @run-at 时机

- `document-start` — 最早注入，适合拦截请求 / 修改全局变量
- `document-end` — DOM 就绪后（≈ DOMContentLoaded），**默认值，最常用**
- `document-idle` — 页面完全加载后

#### 安全

- 避免 `eval()` 和 `innerHTML` 注入不可信内容
- `GM.xmlHttpRequest` 必须配合 `@connect` 声明允许的域名
- 不要在 `@grant none` 模式下使用 `unsafeWindow`（冗余且无沙箱保护）
- 跨域请求不要暴露敏感 token 到日志

### 常见问题排查

| 现象 | 可能原因 | 解决方案 |
|------|----------|----------|
| 脚本不执行 | @match 不匹配当前 URL | 检查 URL 模式，注意 `www` 子域和 `http/https` 协议 |
| DOM 元素找不到 | SPA 动态加载，执行时元素不存在 | 用 MutationObserver 或轮询等待（查 `patterns` 参考） |
| 跨域请求失败 | 未声明 @connect 或未用 GM.xmlHttpRequest | 添加 `@connect domain` 并使用 GM API 而非 fetch |
| `GM_xxx is not defined` | 未在 @grant 中声明 | 添加对应的 `@grant GM_xxx` |
| 页面变量访问不到 | @grant 非 none，脚本在沙箱中 | 使用 `unsafeWindow.变量名` |
| 样式不生效 | CSS 优先级不够 | 加 `!important` 或用 `GM_addStyle` 注入 |
| 脚本执行两次 | @match 重复匹配（iframe） | 加 `if (window.top !== window.self) return;` |

### 示例

**隐藏页面元素**：
```
用户：去掉知乎的登录弹窗
→ @match *://*.zhihu.com/*
→ @grant GM_addStyle
→ GM_addStyle('.Modal-wrapper, .signFlowModal { display: none !important; }');
```

**数据导出**：
```
用户：导出 GitHub trending 项目为 JSON
→ @match https://github.com/trending*
→ @grant GM_setClipboard, GM_registerMenuCommand
→ querySelectorAll 提取 → JSON.stringify → GM_setClipboard
```

**需要页面分析**：
```
用户：自动点赞 B 站视频
→ analyze_page 分析 B 站视频页面，获取点赞按钮选择器
→ 根据分析结果编写点击逻辑
```

**ScriptCat 定时任务**：
```
用户：每天早上 9 点检查某网页是否有更新
→ read_reference("scriptcat-dev", "scriptcat_api")
→ 使用 @crontab 0 9 * * * 实现定时后台检查
```

### Tips

- **优先 Promise 风格**：`GM.xmlHttpRequest` 优于 `GM_xmlhttpRequest`（callback），`GM.getValue` 优于 `GM_getValue`
- **SPA 适配**：用 MutationObserver 监听 DOM 变化，而非 setInterval 轮询
- **CSS 注入**：简单样式用 `GM_addStyle`，大量样式用 `@resource` 引入外部 CSS
- **标注兼容性**：使用 ScriptCat 特有功能时在注释中标注 `// ScriptCat only`
- **框架感知**：`analyze_page` 会报告前端框架（React/Vue 等），虚拟 DOM 框架需注意直接 DOM 操作可能被覆盖
- **调试**：建议用户在浏览器 DevTools Console 中测试选择器，再写入脚本
