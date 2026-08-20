# 高级技巧与最佳实践

> Tampermonkey 高级技术（XHR/fetch 请求拦截、拖拽 UI 面板、键盘快捷键）与最佳实践总结。

### Advanced Techniques

#### Intercepting XHR/Fetch Requests

```javascript
// Intercept and modify fetch requests
(function(fetch) {
    window.fetch = function(...args) {
        console.log('Fetch intercepted:', args[0]);

        // Modify request if needed
        if (args[0].includes('api.example.com')) {
            const modifiedInit = args[1] || {};
            modifiedInit.headers = {
                ...modifiedInit.headers,
                'X-Custom-Header': 'MyValue'
            };
            args[1] = modifiedInit;
        }

        return fetch.apply(this, args)
            .then(response => {
                console.log('Fetch response:', response.url, response.status);
                return response;
            });
    };
})(window.fetch);
```

#### Creating Draggable UI Panels

```javascript
function createDraggablePanel(content) {
    const panel = document.createElement('div');
    panel.innerHTML = `
        <div class="panel-header" style="cursor: move; background: #333; color: white; padding: 10px;">
            Drag Me
            <button class="close-btn" style="float: right;">×</button>
        </div>
        <div class="panel-content" style="background: white; padding: 15px;">
            ${content}
        </div>
    `;

    panel.style.cssText = 'position: fixed; top: 50px; right: 50px; width: 300px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 99999;';

    // Make draggable
    const header = panel.querySelector('.panel-header');
    let isDragging = false;
    let currentX, currentY, initialX, initialY;

    header.addEventListener('mousedown', (e) => {
        isDragging = true;
        initialX = e.clientX - panel.offsetLeft;
        initialY = e.clientY - panel.offsetTop;
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            panel.style.left = currentX + 'px';
            panel.style.top = currentY + 'px';
            panel.style.right = 'auto';
        }
    });

    document.addEventListener('mouseup', () => isDragging = false);

    // Close button
    panel.querySelector('.close-btn').addEventListener('click', () => panel.remove());

    document.body.appendChild(panel);
    return panel;
}

// Usage
createDraggablePanel('<h3>Settings</h3><p>Your content here</p>');
```

#### Keyboard Shortcuts

```javascript
// Register keyboard shortcuts
function registerHotkey(keys, callback) {
    const keysArray = keys.toLowerCase().split('+').map(k => k.trim());

    document.addEventListener('keydown', (e) => {
        const pressed = [];
        if (e.ctrlKey) pressed.push('ctrl');
        if (e.altKey) pressed.push('alt');
        if (e.shiftKey) pressed.push('shift');
        if (e.metaKey) pressed.push('meta');
        pressed.push(e.key.toLowerCase());

        if (pressed.sort().join('+') === keysArray.sort().join('+')) {
            e.preventDefault();
            callback(e);
        }
    });
}

// Usage
registerHotkey('ctrl+shift+x', () => {
    console.log('Hotkey triggered!');
    // Your action here
});
```


### Best Practices Summary

1. **Always declare @grant** - Even if using `none`
2. **Use MutationObserver** - For dynamic content
3. **Cache DOM references** - Query once, use many times
4. **Handle errors gracefully** - Wrap in try-catch blocks
5. **Prefix console logs** - Easy filtering in DevTools
6. **Version your scripts** - Use @version for updates
7. **Document dependencies** - List in @description or comments
8. **Test in incognito** - Catch extension conflicts
9. **Respect site performance** - Don't block rendering
10. **Follow site ToS** - Don't abuse automation

