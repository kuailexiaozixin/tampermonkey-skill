# 运行环境与兼容性

> Tampermonkey 沙箱与安全模式、跨浏览器（Chrome/Firefox/Edge）兼容要点。

## Tampermonkey Sandbox Modes

Understanding script execution contexts and security sandboxing.

---

### Overview

Tampermonkey can inject userscripts into different execution contexts (worlds). The context affects:
- What the script can access
- Security isolation
- CSP (Content Security Policy) restrictions
- How to communicate with the page

---

### Execution Worlds

#### MAIN_WORLD (Page Context)

Script runs in the same context as the page's JavaScript.

**Pros:**
- Direct access to page variables and functions
- No need for unsafeWindow
- Can modify page objects directly

**Cons:**
- Subject to page's CSP
- Can be detected by the page
- Security risks if page is malicious

#### ISOLATED_WORLD (Content Script Context)

Script runs in an isolated context, separate from the page.

**Pros:**
- Protected from page scripts
- Can't be detected easily
- Safer execution

**Cons:**
- Cannot directly access page variables
- Need unsafeWindow for page interaction
- Some APIs may not work

#### USERSCRIPT_WORLD (Firefox Only)

Special context created for userscripts, with enhanced capabilities.

**Pros:**
- Bypasses CSP
- Better isolation than MAIN_WORLD
- Supports document-start timing

**Cons:**
- Firefox only
- Need cloneInto/exportFunction for page communication

---

### @sandbox Directive

Control where your script runs using @sandbox.

#### @sandbox raw

Request to run in page context (MAIN_WORLD).

```javascript
// @sandbox raw

// Direct page access
console.log(window.pageVariable);  // Works
pageFunction();  // Works
```

**Use when:**
- You need direct page variable access
- Page CSP doesn't block inline scripts
- You don't need isolation

#### @sandbox JavaScript

Request access to unsafeWindow. May use USERSCRIPT_WORLD on Firefox.

```javascript
// @sandbox JavaScript

// Access page through unsafeWindow
console.log(unsafeWindow.pageVariable);
unsafeWindow.pageFunction();
```

**Use when:**
- You need unsafeWindow access
- You want CSP bypass (Firefox)
- Default for most scripts needing page interaction

#### @sandbox DOM

Only need DOM access, no page JavaScript access.

```javascript
// @sandbox DOM

// DOM access works
document.querySelector('#element').textContent = 'Modified';

// Page variables are NOT accessible
// window.pageVariable is undefined
```

**Use when:**
- Only modifying DOM/CSS
- Don't need page JavaScript access
- Want maximum isolation

---

### @grant none

Disables the sandbox entirely.

```javascript
// @grant none

// Runs in page context
// No GM_* functions available (except GM_info)
console.log(window.pageVariable);  // Direct access
```

**When to use:**
- Simple scripts that don't need GM_* APIs
- Direct page integration needed
- Smallest footprint

**What you lose:**
- All GM_* functions (except GM_info)
- Cross-origin requests
- Persistent storage
- CSP bypass

---

### Firefox: cloneInto and exportFunction

When running in USERSCRIPT_WORLD, you need special functions to share data with the page.

#### cloneInto

Clone an object so the page can access it.

```javascript
// Share data with page
const data = { name: 'John', count: 42 };
unsafeWindow.myData = cloneInto(data, unsafeWindow);

// Clone with functions
const obj = { getValue: () => 42 };
unsafeWindow.myObj = cloneInto(obj, unsafeWindow, { cloneFunctions: true });
```

#### exportFunction

Export a function so the page can call it.

```javascript
// Export a function
function myHandler(arg) {
    console.log('Called with:', arg);
    return 'response';
}

unsafeWindow.myHandler = exportFunction(myHandler, unsafeWindow);

// Page can now call: myHandler('hello')
```

#### Complete Example

```javascript
// @sandbox JavaScript

// Create an API for the page
const scriptAPI = {
    version: '1.0.0',
    getData: function() {
        return GM_getValue('data', null);
    },
    setData: function(data) {
        GM_setValue('data', data);
    }
};

// Export to page
if (typeof cloneInto !== 'undefined') {
    // Firefox - need to export
    unsafeWindow.ScriptAPI = cloneInto(scriptAPI, unsafeWindow, {
        cloneFunctions: true
    });
} else {
    // Chrome - direct assignment works
    unsafeWindow.ScriptAPI = scriptAPI;
}
```

---

### Content Security Policy (CSP)

#### What CSP Blocks

CSP can prevent:
- Inline `<script>` tags
- eval() and new Function()
- Inline event handlers
- Loading scripts from non-whitelisted domains

#### How Tampermonkey Bypasses CSP

| Context | CSP Bypass |
|---------|------------|
| MAIN_WORLD | No - subject to CSP |
| ISOLATED_WORLD | Partial - script runs, but injected scripts may be blocked |
| USERSCRIPT_WORLD | Yes - bypasses CSP |

#### Techniques for CSP Issues

**Use GM_addElement instead of createElement:**

```javascript
// This may be blocked by CSP:
const script = document.createElement('script');
script.textContent = 'console.log("blocked")';
document.head.appendChild(script);

// This bypasses CSP:
GM_addElement('script', {
    textContent: 'console.log("works")'
});
```

**Use @require for external scripts:**

```javascript
// Instead of dynamically loading scripts, use @require
// @require https://code.jquery.com/jquery-3.6.0.min.js
```

---

### Content Script API Setting

In Tampermonkey settings, you can configure how scripts are injected:

#### Content Script (Default)

- Scripts injected via content script API
- Retrieved via messaging
- No true document-start support

#### UserScripts API

- Uses browser's UserScripts API
- Chrome: via messaging, no document-start
- Firefox: instant execution, document-start works

#### UserScripts API Dynamic

- Both wrapper and script injected via API
- True document-start support
- Most compatible

---

### Detecting the Current Context

```javascript
// Check if in isolated world
const isIsolated = typeof cloneInto !== 'undefined';

// Check sandbox mode from GM_info
console.log('Sandbox mode:', GM_info.sandboxMode);
// Values: 'js', 'raw', 'dom'

// Check if page objects are directly accessible
const hasDirectAccess = window.somePageVariable !== undefined;
```

---

### Best Practices

#### 1. Start with @sandbox DOM

If you only need DOM access, use the most restrictive mode:

```javascript
// @sandbox DOM
// Most isolated, safest
```

#### 2. Use @sandbox JavaScript for page interaction

```javascript
// @sandbox JavaScript
// Access page via unsafeWindow
const pageData = unsafeWindow.APP_CONFIG;
```

#### 3. Handle cross-browser differences

```javascript
// Works in all contexts
function shareWithPage(name, value) {
    if (typeof cloneInto !== 'undefined') {
        // Firefox USERSCRIPT_WORLD
        unsafeWindow[name] = cloneInto(value, unsafeWindow, {
            cloneFunctions: true
        });
    } else {
        // Chrome or MAIN_WORLD
        unsafeWindow[name] = value;
    }
}
```

#### 4. Test in multiple browsers

Different browsers may behave differently. Test in:
- Chrome (Manifest V3)
- Firefox
- Edge
- Safari (if using Userscripts app)

---

## Browser Compatibility Guide

Cross-browser differences and compatibility matrix for Tampermonkey userscripts.

---

### Browser Support Matrix

| Feature | Chrome | Firefox | Edge | Safari | Opera |
|---------|--------|---------|------|--------|-------|
| **Tampermonkey** | ✅ | ✅ | ✅ | ⚠️ Userscripts app | ✅ |
| **Manifest Version** | V3 | V2 | V3 | N/A | V3 |

#### API Compatibility

| API | Chrome | Firefox | Edge | Notes |
|-----|--------|---------|------|-------|
| `GM_setValue/getValue` | ✅ | ✅ | ✅ | Universal |
| `GM_xmlhttpRequest` | ✅ | ✅ | ✅ | Universal |
| `GM_addStyle` | ✅ | ✅ | ✅ | Universal |
| `GM_addElement` | ✅ | ✅ | ✅ | Universal |
| `GM_notification` | ✅ | ✅ | ✅ | Universal |
| `GM_download` | ✅ | ✅ | ✅ | Universal |
| `GM_openInTab` | ✅ | ✅ | ✅ | Universal |
| `GM_registerMenuCommand` | ✅ | ✅ | ✅ | Universal |
| `GM_cookie` | ✅ | ✅ | ✅ | Universal |
| `GM_webRequest` | ❌ MV3 | ✅ | ❌ MV3 | Firefox only now |
| `GM_audio` | ✅ | ✅ | ✅ | v5.0+ |
| `window.onurlchange` | ✅ | ✅ | ✅ | Universal |
| `unsafeWindow` | ✅ | ✅ | ✅ | Universal |

#### Sandbox & Execution Context

| Feature | Chrome | Firefox | Notes |
|---------|--------|---------|-------|
| `@sandbox raw` | ✅ | ✅ | Page context |
| `@sandbox JavaScript` | ✅ | ✅ USERSCRIPT_WORLD | Firefox has special context |
| `@sandbox DOM` | ✅ | ✅ | Isolated context |
| `document-start` timing | ⚠️ | ✅ | Firefox more reliable |
| `cloneInto` | ❌ | ✅ | Firefox only |
| `exportFunction` | ❌ | ✅ | Firefox only |

---

### Manifest V3 Limitations (Chrome/Edge)

Chrome and Edge use Manifest V3, which restricts certain features:

#### What Doesn't Work in MV3

1. **@webRequest** - Request interception is blocked
2. **Some background script patterns** - Persistent background pages removed
3. **Certain CSP bypass methods** - More restricted

#### Workarounds

```javascript
// Instead of @webRequest, use page-level interception
// @grant unsafeWindow

// Intercept fetch
const originalFetch = unsafeWindow.fetch;
unsafeWindow.fetch = function(...args) {
    console.log('Intercepted fetch:', args[0]);
    return originalFetch.apply(this, args);
};

// Intercept XMLHttpRequest
const originalOpen = unsafeWindow.XMLHttpRequest.prototype.open;
unsafeWindow.XMLHttpRequest.prototype.open = function(method, url) {
    console.log('Intercepted XHR:', method, url);
    return originalOpen.apply(this, arguments);
};
```

---

### Firefox-Specific Features

#### cloneInto and exportFunction

Firefox's USERSCRIPT_WORLD requires special functions to share data with the page.

```javascript
// Share object with page (Firefox)
function shareWithPage(name, value) {
    if (typeof cloneInto !== 'undefined') {
        // Firefox - must use cloneInto
        unsafeWindow[name] = cloneInto(value, unsafeWindow, {
            cloneFunctions: true
        });
    } else {
        // Chrome - direct assignment works
        unsafeWindow[name] = value;
    }
}

// Export function for page to call (Firefox)
function exportToPage(name, fn) {
    if (typeof exportFunction !== 'undefined') {
        // Firefox
        unsafeWindow[name] = exportFunction(fn, unsafeWindow);
    } else {
        // Chrome
        unsafeWindow[name] = fn;
    }
}

// Usage
shareWithPage('myData', { count: 42, items: ['a', 'b'] });
exportToPage('myFunction', (arg) => console.log('Called with:', arg));
```

#### Firefox Containers

Firefox supports container tabs for privacy isolation.

```javascript
// @run-in container-id-2
// @run-in container-id-3

// Get container ID at runtime
console.log('Container:', GM_info.container);
// { id: "2", name: "Personal" }
```

---

### Safari Support

Safari uses a third-party app called "Userscripts" (not Tampermonkey).

#### Key Differences

| Feature | Safari Userscripts | Tampermonkey |
|---------|-------------------|--------------|
| Installation | Mac App Store | Browser extension |
| @grant support | Limited | Full |
| GM_* APIs | Subset | Full |
| Auto-update | Manual | Automatic |

#### Writing Safari-Compatible Scripts

```javascript
// Check if running in Safari Userscripts app
const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

// Use only widely-supported APIs
// @grant GM_getValue
// @grant GM_setValue
// @grant GM_xmlhttpRequest

// Avoid Safari-incompatible features
// @grant GM_webRequest  // May not work
// @grant GM_audio       // May not work
```

---

### Cross-Browser Best Practices

#### 1. Feature Detection

```javascript
// Check if API exists before using
if (typeof GM_notification !== 'undefined') {
    GM_notification('Hello!');
} else {
    alert('Hello!');  // Fallback
}

// Check for Firefox-specific features
const isFirefox = typeof cloneInto !== 'undefined';
```

#### 2. Graceful Degradation

```javascript
// Provide fallbacks for unsupported features
async function showNotification(message) {
    if (typeof GM_notification !== 'undefined') {
        GM_notification({ text: message });
    } else if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(message);
    } else {
        console.log('Notification:', message);
    }
}
```

#### 3. Avoid Browser-Specific Code

```javascript
// Wrong - breaks in other browsers
if (navigator.userAgent.includes('Firefox')) {
    // Firefox-specific code
}

// Right - feature detection
if (typeof exportFunction !== 'undefined') {
    // Use exportFunction
} else {
    // Use alternative
}
```

#### 4. Test in Multiple Browsers

Before releasing a script:

1. ✅ Test in Chrome (most common)
2. ✅ Test in Firefox (second most common)
3. ✅ Test in Edge (uses same engine as Chrome)
4. ⚠️ Test in Safari if targeting Mac users

---

### Browser-Specific Bugs & Workarounds

#### Chrome: document-start Timing

Chrome's document-start isn't always reliable.

```javascript
// @run-at document-start

// May not run early enough - add fallback
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();  // Already loaded
}
```

#### Firefox: Strict CSP Sites

Some sites have strict CSP that even Tampermonkey can't bypass.

```javascript
// If GM_addElement fails, try @require instead
// @require https://example.com/library.js

// Or inject via unsafeWindow
unsafeWindow.eval('console.log("injected")');  // Last resort
```

#### Edge: Extension Sync Issues

Edge sometimes doesn't sync Tampermonkey settings.

**Workaround:** Export/import settings manually between devices.

---

### Version Requirements

Some features require specific Tampermonkey versions:

| Feature | Minimum Version |
|---------|-----------------|
| `GM.* async APIs` | 4.0+ |
| `GM_audio` | 5.0+ |
| `@tag` | 5.0+ |
| `GM_notification.tag` | 5.0+ |
| `@run-in` | 5.3+ |
| `GM_setValues/getValues` | 5.3+ |

```javascript
// Check Tampermonkey version
const version = GM_info.version;
console.log('Tampermonkey version:', version);

// Feature detection is safer than version checking
if (typeof GM_audio !== 'undefined') {
    // Use GM_audio
}
```
