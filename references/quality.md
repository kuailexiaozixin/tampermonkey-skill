# 质量与调试

> 用户脚本调试清单、常见坑排查、安全交付检查清单。

## Debugging Userscripts

How to troubleshoot and fix broken userscripts.

---

### Quick Diagnostic Checklist

When a script doesn't work, check these first:

```
[ ] 1. Is the script enabled in Tampermonkey dashboard?
[ ] 2. Does the @match pattern match the current URL?
[ ] 3. Are there errors in the browser console? (F12)
[ ] 4. Are all required @grant statements present?
[ ] 5. Does @connect include all external domains?
[ ] 6. Is the element present when the script runs?
```

---

### Viewing Script Errors

#### Browser Console (Recommended)

1. Press **F12** to open DevTools
2. Go to **Console** tab
3. Look for red error messages
4. Filter by "userscript" if needed

#### Tampermonkey Dashboard

1. Click Tampermonkey icon → **Dashboard**
2. Look for scripts with error indicators
3. Click script name → **Editor** to see inline errors

---

### Testing if Script Runs

#### Method 1: Alert (Most Obvious)

```javascript
// ==UserScript==
// @name         Test Script
// @match        https://example.com/*
// ==/UserScript==

alert('Script is running!');  // Will definitely show if script loads
```

#### Method 2: Console Log

```javascript
console.log('=== USERSCRIPT LOADED ===');
console.log('URL:', location.href);
console.log('Time:', new Date().toISOString());
```

#### Method 3: Visual Indicator

```javascript
// @grant GM_addStyle

GM_addStyle(`
    body::before {
        content: 'Script Active';
        position: fixed;
        top: 0;
        right: 0;
        background: green;
        color: white;
        padding: 5px 10px;
        z-index: 999999;
        font-size: 12px;
    }
`);
```

---

### Common Error Messages

#### "Cannot read property 'X' of null"

**Cause:** Element doesn't exist when script runs.

```javascript
// Error
document.querySelector('#missing').textContent = 'Hi';

// Fix: Check if element exists
const el = document.querySelector('#missing');
if (el) {
    el.textContent = 'Hi';
} else {
    console.log('Element not found');
}

// Better fix: Wait for element
waitForElement('#missing').then(el => {
    el.textContent = 'Hi';
});
```

#### "GM_xxx is not defined"

**Cause:** Missing @grant statement.

```javascript
// Error - forgot @grant
GM_setValue('key', 'value');  // ReferenceError

// Fix - add @grant
// @grant GM_setValue
GM_setValue('key', 'value');  // Works
```

#### "Access to XMLHttpRequest blocked by CORS"

**Cause:** Using native fetch/XHR instead of GM_xmlhttpRequest.

```javascript
// Error - blocked by CORS
fetch('https://api.example.com/data');

// Fix - use GM_xmlhttpRequest
// @grant GM_xmlhttpRequest
// @connect api.example.com

GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => console.log(r.responseText)
});
```

#### "Content Security Policy" errors

**Cause:** Site's CSP blocks inline scripts.

```javascript
// Error - blocked by CSP
const script = document.createElement('script');
script.textContent = 'console.log("blocked")';
document.head.appendChild(script);

// Fix - use GM_addElement
// @grant GM_addElement
GM_addElement('script', {
    textContent: 'console.log("works")'
});
```

---

### Debugging Techniques

#### 1. Isolate the Problem

Comment out sections to find what's breaking:

```javascript
console.log('Step 1');
// doSomething();

console.log('Step 2');
// doSomethingElse();

console.log('Step 3');
// maybeBroken();  // Uncomment one at a time
```

#### 2. Log Variables

```javascript
const element = document.querySelector('#target');
console.log('Element:', element);
console.log('Element exists:', !!element);
console.log('Element HTML:', element?.outerHTML);
```

#### 3. Breakpoints

```javascript
// Pause execution here
debugger;

// Or set breakpoints in DevTools:
// 1. F12 → Sources tab
// 2. Find your script (search for script name)
// 3. Click line number to set breakpoint
```

#### 4. Network Tab

For GM_xmlhttpRequest issues:

1. F12 → **Network** tab
2. Look for your request
3. Check **Headers**, **Response**, **Timing**
4. Red = failed request

#### 5. Test @match Pattern

```javascript
// Log when script runs to verify @match
console.log('Script matched:', location.href);

// Test pattern manually:
// @match https://example.com/*
// Should match: https://example.com/page
// Should NOT match: https://other.com/example.com
```

---

### Debugging Async Code

#### Problem: Callback Not Firing

```javascript
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (response) => {
        console.log('Response received');  // Never logs
    }
});

// Debug: Add all callbacks
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => console.log('Success:', r.status),
    onerror: (e) => console.log('Error:', e),
    ontimeout: () => console.log('Timeout'),
    onabort: () => console.log('Aborted')
});
```

#### Problem: Promise Never Resolves

```javascript
// Stuck promise
const data = await someAsyncFunction();  // Never continues

// Debug: Add timeout
const data = await Promise.race([
    someAsyncFunction(),
    new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Timeout after 10s')), 10000)
    )
]);
```

---

### Debugging Element Waiting

#### Check if Element Ever Appears

```javascript
// Watch for element in console
const observer = new MutationObserver((mutations) => {
    const el = document.querySelector('#target');
    if (el) {
        console.log('FOUND:', el);
        observer.disconnect();
    }
});
observer.observe(document.body, { childList: true, subtree: true });

// After 30 seconds, report if not found
setTimeout(() => {
    if (document.querySelector('#target') === null) {
        console.log('Element never appeared after 30s');
        console.log('Current DOM:', document.body.innerHTML.substring(0, 1000));
    }
}, 30000);
```

---

### Debugging Storage

#### Verify Values Are Saved

```javascript
// Save
GM_setValue('test', { foo: 'bar' });
console.log('Saved');

// Read back immediately
const value = GM_getValue('test');
console.log('Retrieved:', value);
console.log('Type:', typeof value);

// List all keys
const keys = GM_listValues();
console.log('All keys:', keys);
```

#### Clear Storage for Fresh Start

```javascript
// Delete all stored values
GM_listValues().forEach(key => {
    console.log('Deleting:', key);
    GM_deleteValue(key);
});
```

---

### Browser-Specific Debugging

#### Chrome DevTools Tips

- **Sources** → **Content Scripts** shows userscripts
- **Application** → **Storage** shows extension data
- Use **Snippets** to test code quickly

#### Firefox DevTools Tips

- **Debugger** → Search for script name
- About:debugging → This Firefox → Tampermonkey → Inspect
- Firefox shows better error messages for cloneInto issues

---

### Getting Help

If you can't solve the issue:

1. **Check Tampermonkey forums** - Search for similar issues
2. **Provide minimal reproduction** - Smallest script that shows the bug
3. **Include browser/TM version** - Found in GM_info
4. **Share console errors** - Copy the exact error message

```javascript
// Get debug info to share
console.log('Browser:', navigator.userAgent);
console.log('Tampermonkey:', GM_info.version);
console.log('Script:', GM_info.script.name, GM_info.script.version);
```

---

## Common Userscript Pitfalls

Mistakes that break userscripts and how to avoid them.

---

### Pitfall 1: @match Too Broad

Running on every page slows the browser and causes unexpected behaviour.

**Wrong:**
```javascript
// @match *://*/*
// @match https://*/*
```

**Right:**
```javascript
// @match https://example.com/*
// @match https://*.example.com/*
```

**Why it matters:** Overly broad patterns mean your script runs on thousands of sites, consuming memory and potentially breaking pages.

---

### Pitfall 2: Missing @connect

Cross-origin requests fail silently or show permission dialogs without @connect.

**Wrong:**
```javascript
// @grant GM_xmlhttpRequest
// No @connect declaration

GM_xmlhttpRequest({
    url: 'https://api.example.com/data',  // Will prompt or fail
    ...
});
```

**Right:**
```javascript
// @grant GM_xmlhttpRequest
// @connect api.example.com

GM_xmlhttpRequest({
    url: 'https://api.example.com/data',  // Works
    ...
});
```

**Best practice:** Declare all known domains, then add `@connect *` as fallback.

---

### Pitfall 3: Not Waiting for Elements

Elements may not exist when your script runs, especially on SPAs.

**Wrong:**
```javascript
// @run-at document-end

// Element might not exist yet!
document.querySelector('#dynamic-content').textContent = 'Modified';
// TypeError: Cannot read property 'textContent' of null
```

**Right:**
```javascript
// Use waitForElement pattern
async function init() {
    const element = await waitForElement('#dynamic-content');
    element.textContent = 'Modified';
}

function waitForElement(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const el = document.querySelector(selector);
        if (el) return resolve(el);

        const observer = new MutationObserver((_, obs) => {
            const el = document.querySelector(selector);
            if (el) {
                obs.disconnect();
                resolve(el);
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
        setTimeout(() => {
            observer.disconnect();
            reject(new Error(`Timeout: ${selector}`));
        }, timeout);
    });
}

init();
```

---

### Pitfall 4: Blocking Async Operations

GM_xmlhttpRequest is asynchronous - you can't use its return value directly.

**Wrong:**
```javascript
const response = GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.example.com/data'
});
console.log(response.responseText);  // undefined!
```

**Right (callback):**
```javascript
GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.example.com/data',
    onload: function(response) {
        console.log(response.responseText);  // Works
    }
});
```

**Right (async/await with GM.*):**
```javascript
const response = await GM.xmlHttpRequest({
    method: 'GET',
    url: 'https://api.example.com/data'
});
console.log(response.responseText);  // Works
```

---

### Pitfall 5: CSP Blocking Script Injection

Content Security Policy blocks dynamically created scripts.

**Wrong:**
```javascript
const script = document.createElement('script');
script.textContent = 'console.log("blocked by CSP")';
document.head.appendChild(script);  // Blocked!
```

**Right:**
```javascript
// @grant GM_addElement

GM_addElement('script', {
    textContent: 'console.log("bypasses CSP")'
});
```

---

### Pitfall 6: Sandbox Context Confusion

Without unsafeWindow, you can't access page variables.

**Wrong:**
```javascript
// @grant none

// Trying to access page's React app
console.log(window.React);  // undefined in sandbox
```

**Right:**
```javascript
// @grant unsafeWindow

console.log(unsafeWindow.React);  // Works
```

**Note:** `@grant none` disables the sandbox entirely (different approach).

---

### Pitfall 7: Memory Leaks in Observers

MutationObservers that never disconnect consume memory.

**Wrong:**
```javascript
const observer = new MutationObserver(() => {
    processNewContent();
});
observer.observe(document.body, { childList: true, subtree: true });
// Never disconnected - runs forever!
```

**Right:**
```javascript
const observer = new MutationObserver(() => {
    if (shouldStop()) {
        observer.disconnect();
        return;
    }
    processNewContent();
});
observer.observe(document.body, { childList: true, subtree: true });

// Or disconnect on page unload
window.addEventListener('beforeunload', () => observer.disconnect());
```

---

### Pitfall 8: Overly Aggressive DOM Modifications

Modifying the DOM too frequently causes performance issues.

**Wrong:**
```javascript
// Runs on EVERY mutation
const observer = new MutationObserver(() => {
    document.querySelectorAll('.item').forEach(el => {
        el.style.color = 'red';  // Runs thousands of times
    });
});
```

**Right:**
```javascript
// Debounce modifications
let timeout;
const observer = new MutationObserver(() => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        document.querySelectorAll('.item:not(.processed)').forEach(el => {
            el.style.color = 'red';
            el.classList.add('processed');
        });
    }, 100);
});
```

---

### Pitfall 9: Forgetting Error Handling

Network requests and async operations can fail.

**Wrong:**
```javascript
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => {
        const data = JSON.parse(r.responseText);  // Crashes if invalid JSON
        process(data);
    }
});
```

**Right:**
```javascript
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => {
        try {
            const data = JSON.parse(r.responseText);
            process(data);
        } catch (e) {
            console.error('Failed to parse response:', e);
        }
    },
    onerror: (e) => {
        console.error('Request failed:', e);
    },
    ontimeout: () => {
        console.error('Request timed out');
    }
});
```

---

### Pitfall 10: Global Variable Pollution

Variables leak into page scope without IIFE wrapper.

**Wrong:**
```javascript
// ==UserScript==
// ...
// ==/UserScript==

var myData = 'secret';  // Visible to page as window.myData!
function process() { ... }  // Visible to page
```

**Right:**
```javascript
// ==UserScript==
// ...
// ==/UserScript==

(function() {
    'use strict';

    var myData = 'secret';  // Private to script
    function process() { ... }  // Private to script
})();
```

---

### Pitfall 11: Wrong Timing with @run-at

Script runs before elements exist.

**Wrong:**
```javascript
// @run-at document-start

document.querySelector('#header').remove();  // null - DOM doesn't exist yet!
```

**Right:**
```javascript
// @run-at document-end

document.querySelector('#header').remove();  // Works
```

**Or wait for DOM:**
```javascript
// @run-at document-start

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#header').remove();
});
```

---

### Pitfall 12: Cross-Browser Differences

Firefox and Chrome behave differently.

**Firefox-only features:**
```javascript
// cloneInto and exportFunction only exist in Firefox
if (typeof cloneInto !== 'undefined') {
    unsafeWindow.myData = cloneInto(data, unsafeWindow);
} else {
    unsafeWindow.myData = data;  // Chrome
}
```

**Manifest V3 limitations (Chrome):**
```javascript
// @webRequest doesn't work in Chrome MV3
// Use alternative approaches or inform user
```

---

### Pitfall 13: Hardcoded Selectors

Page structure changes break scripts.

**Fragile:**
```javascript
document.querySelector('div.sc-1234abcd > div:nth-child(3) > span');
```

**Robust:**
```javascript
// Use stable attributes
document.querySelector('[data-testid="username"]');
document.querySelector('[aria-label="Close"]');

// Or multiple fallbacks
const element = document.querySelector('#username') ||
                document.querySelector('[data-user]') ||
                document.querySelector('.profile-name');
```

---

### Pitfall 14: Not Testing in Target Browser

Scripts that work in Chrome may break in Firefox.

**Before deploying:**
1. Test in Chrome
2. Test in Firefox
3. Test in private/incognito mode
4. Test with page's CSP (disable extensions to check)

---

### Pitfall 15: Script Not Running After Tampermonkey v5.4.1 Update

Tampermonkey v5.4.1+ requires explicit user permission to inject scripts into pages.

**Symptom:** Script was working, stopped after Tampermonkey updated.

**Fix:** Click the Tampermonkey icon → "Allow extension to access this site" (or configure globally in Dashboard → Settings → Script Injection).

**Why this changed:** Browser vendors (Chrome MV3) now require extensions to request explicit permission before injecting content into pages.

---

### Quick Diagnostic Checklist

When a script doesn't work:

```
[ ] Console shows errors? (F12 → Console)
[ ] Script is enabled in Tampermonkey dashboard?
[ ] @match pattern matches current URL?
[ ] Required @grant statements present?
[ ] @connect includes target domains?
[ ] Element exists when script runs?
[ ] Using async correctly (callbacks/await)?
[ ] Browser-specific features used correctly?
```

---

## Security Checklist for Userscripts

Pre-delivery validation to ensure scripts are secure and well-formed.

---

### Critical Security Checks

These issues can expose users to serious risks.

#### 1. No Hardcoded Secrets

**Check:** Script contains no API keys, tokens, or passwords.

```javascript
// DANGEROUS - exposed credentials
const API_KEY = 'sk-1234567890abcdef';
const AUTH_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIs...';

// SAFE - user provides credentials
const API_KEY = GM_getValue('apiKey', '');
if (!API_KEY) {
    alert('Please set your API key in the script settings');
}
```

#### 2. @match Not Overly Broad

**Check:** Script doesn't run on all websites unnecessarily.

```javascript
// DANGEROUS - runs everywhere
// @match *://*/*
// @match https://*/*

// SAFE - specific targets
// @match https://example.com/*
// @match https://*.example.com/*
```

#### 3. User Input Sanitised

**Check:** User-provided data is sanitised before DOM insertion.

```javascript
// DANGEROUS - XSS vulnerability
const userInput = prompt('Enter name:');
element.innerHTML = `Hello, ${userInput}!`;  // Can inject HTML/JS

// SAFE - use textContent
element.textContent = `Hello, ${userInput}!`;

// SAFE - escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
element.innerHTML = `Hello, ${escapeHtml(userInput)}!`;
```

#### 4. HTTPS for External Requests

**Check:** All external URLs use HTTPS.

```javascript
// DANGEROUS - HTTP can be intercepted
// @connect http://api.example.com
GM_xmlhttpRequest({ url: 'http://api.example.com/data' });

// SAFE - HTTPS encrypted
// @connect api.example.com
GM_xmlhttpRequest({ url: 'https://api.example.com/data' });
```

#### 5. No eval() or new Function()

**Check:** Script doesn't execute arbitrary code.

```javascript
// DANGEROUS - code injection risk
eval(userInput);
new Function(userInput)();
setTimeout(userInput, 1000);  // If userInput is a string

// SAFE - use proper callbacks
setTimeout(() => doSomething(), 1000);
```

---

### Header Validation

#### Required Headers

```javascript
// ==UserScript==
// @name         ✓ Descriptive and unique
// @namespace    ✓ Your unique identifier
// @version      ✓ Semantic version (1.0.0)
// @description  ✓ Clear description
// @author       ✓ Your name
// @match        ✓ Specific URL patterns
// @grant        ✓ Only needed permissions
// ==/UserScript==
```

#### Permission Minimisation

**Check:** Only necessary @grant statements are included.

```javascript
// BAD - excessive permissions
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_xmlhttpRequest
// @grant GM_notification
// @grant unsafeWindow
// @grant GM_download
// @grant GM_cookie

// GOOD - only what's needed
// @grant GM_addStyle
// (Script only modifies CSS)
```

#### @connect Validation

**Check:** All @connect domains are legitimate and expected.

```javascript
// Verify each domain is needed
// @connect api.example.com      ✓ Main API
// @connect cdn.example.com      ✓ CDN resources
// @connect tracking.ads.com     ✗ Why is this here?
```

---

### Code Quality Checks

#### 1. IIFE Wrapper

**Check:** Script is wrapped to prevent global pollution.

```javascript
// REQUIRED
(function() {
    'use strict';
    // Script code here
})();
```

#### 2. Error Handling

**Check:** Async operations have error handlers.

```javascript
// BAD - no error handling
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => process(JSON.parse(r.responseText))
});

// GOOD - comprehensive error handling
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => {
        try {
            const data = JSON.parse(r.responseText);
            process(data);
        } catch (e) {
            console.error('Parse error:', e);
        }
    },
    onerror: (e) => console.error('Request failed:', e),
    ontimeout: () => console.error('Request timed out')
});
```

#### 3. Null Checks

**Check:** DOM queries check for null before use.

```javascript
// BAD - crashes if element missing
document.querySelector('#target').click();

// GOOD - safe access
const el = document.querySelector('#target');
if (el) {
    el.click();
}

// BETTER - optional chaining
document.querySelector('#target')?.click();
```

---

### Performance Checks

#### 1. No Infinite Loops

**Check:** Loops have proper exit conditions.

```javascript
// DANGEROUS - potential infinite loop
while (true) {
    if (condition) break;
}

// SAFE - bounded iterations
for (let i = 0; i < 1000; i++) {
    if (condition) break;
}
```

#### 2. Observer Cleanup

**Check:** MutationObservers are disconnected when done.

```javascript
// BAD - runs forever
const observer = new MutationObserver(callback);
observer.observe(document.body, { childList: true, subtree: true });

// GOOD - disconnects when appropriate
const observer = new MutationObserver((mutations, obs) => {
    if (foundTarget) {
        obs.disconnect();
    }
});
```

#### 3. Debounced Operations

**Check:** Frequent operations are throttled.

```javascript
// BAD - runs on every mutation
observer.observe(document.body, { childList: true, subtree: true });

// GOOD - debounced
let timeout;
const observer = new MutationObserver(() => {
    clearTimeout(timeout);
    timeout = setTimeout(processChanges, 100);
});
```

---

### Pre-Delivery Checklist

Before returning a userscript, verify:

#### Critical (Must Pass)

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] @match is specific (not `*://*/*`)
- [ ] All external URLs use HTTPS
- [ ] User input is sanitised before DOM insertion
- [ ] No eval() or string-based setTimeout/setInterval

#### Important (Should Pass)

- [ ] Wrapped in IIFE with 'use strict'
- [ ] All @grant statements are necessary
- [ ] @connect includes all external domains
- [ ] Error handling for async operations
- [ ] Null checks before DOM manipulation

#### Recommended (Nice to Have)

- [ ] @version follows semantic versioning
- [ ] MutationObservers are cleaned up
- [ ] Frequent operations are debounced
- [ ] Comments explain non-obvious code
- [ ] Works in both Chrome and Firefox

---

### Security Red Flags

Immediately question scripts that:

| Red Flag | Concern |
|----------|---------|
| `@match *://*/*` | Why does it need to run everywhere? |
| `@grant unsafeWindow` | Does it really need page context? |
| `eval()` or `new Function()` | Code injection risk |
| Hardcoded URLs to unknown domains | Data exfiltration? |
| `@connect *` without explanation | Where is data going? |
| Minified/obfuscated code | What is it hiding? |
| Requests to IP addresses | Suspicious destination |
| localStorage/cookie access without clear purpose | Data harvesting? |

---

### Safe Patterns

#### Safe Data Storage

```javascript
// Use GM storage, not localStorage
GM_setValue('userPrefs', { theme: 'dark' });
const prefs = GM_getValue('userPrefs', {});
```

#### Safe External Requests

```javascript
// Validate response before use
GM_xmlhttpRequest({
    url: 'https://api.example.com/data',
    onload: (r) => {
        if (r.status !== 200) {
            console.error('Unexpected status:', r.status);
            return;
        }

        let data;
        try {
            data = JSON.parse(r.responseText);
        } catch (e) {
            console.error('Invalid JSON');
            return;
        }

        if (!data.expected_field) {
            console.error('Missing expected field');
            return;
        }

        process(data);
    }
});
```

#### Safe DOM Insertion

```javascript
// Create elements programmatically
const div = document.createElement('div');
div.textContent = userInput;  // Safe - no HTML parsing
div.className = 'my-class';
document.body.appendChild(div);
```
