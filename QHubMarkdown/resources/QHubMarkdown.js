// Initialize the markdown renderer
function initializeMarkdownRenderer() {
    // Configure Marked
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(code, { language: lang }).value;
                } catch (e) {
                    console.error(e);
                }
            }
            return hljs.highlightAuto(code).value;
        },
        langPrefix: 'hljs language-',
    });

    // Store the current markdown text
    window.currentMarkdownText = "";

    // Function to python
    window.writeMarkdown = function(md) {
        window.currentMarkdownText = md;
        document.getElementById('content').innerHTML = marked.parse(md);
        // Apply syntax highlighting to all code blocks
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        // Avoid redirects within the embedded browser
        if (!window.embeddedRedirection) {
            avoidRedirections();
        }
        // Immediately update the bridge with the new text
        if (window.markdownBridge) {
            window.markdownBridge.setMarkdownText(window.currentMarkdownText);
        }
    };

    // Function to python
    window.insertMarkdown = function(md) {
        window.currentMarkdownText += md;
        document.getElementById('content').innerHTML += marked.parse(md);
        // Apply syntax highlighting to all code blocks
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        // Avoid redirects within the embedded browser
        if (!window.embeddedRedirection) {
            avoidRedirections();
        }
        // Immediately update the bridge with the new text
        if (window.markdownBridge) {
            window.markdownBridge.setMarkdownText(window.currentMarkdownText);
        }
    };

    // Function to python
    window.clearMarkdown = function() {
        window.currentMarkdownText = "";
        document.getElementById('content').innerHTML = '';
        // Immediately update the bridge with the cleared text
        if (window.markdownBridge) {
            window.markdownBridge.setMarkdownText(window.currentMarkdownText);
        }
    };

    // Function to get markdown text (for webchannel)
    window.getMarkdownText = function() {
        if (window.markdownBridge) {
            window.markdownBridge.setMarkdownText(window.currentMarkdownText);
        }
    };

    // Signal that the renderer is ready
    window.markdownRendererReady = true;

    // Possibility of native redirection
    window.embeddedRedirection = false;

    // Function to enable or dissable link redirection with embedded browser
    window.setNativeRedirection = function(state) {
        window.embeddedRedirection = state;
    };
}

// Wait for all resources to load
window.addEventListener('load', function() {
    initializeMarkdownRenderer();
    
    // Setup WebChannel connection
    if (typeof QWebChannel !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.markdownBridge = channel.objects.markdownBridge;
            
            // Connect to the signal for requesting markdown text
            if (window.markdownBridge) {
                window.markdownBridge.markdownTextRequested.connect(function() {
                    window.getMarkdownText();
                });
            }
        });
    }
});

// Avoid redirects within the embedded browser
function avoidRedirections() {
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            alert('You cannot navigate from here. If you need embedded navigation (it is not recommended), use: setNativeRedirection(True).');
        });
    });
}