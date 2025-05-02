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

    // Function to python
    window.writeMarkdown = function(md) {
        document.getElementById('content').innerHTML = marked.parse(md);
        // Apply syntax highlighting to all code blocks
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        // Avoid redirects within the embedded browser
        if (!window.embeddedRedirection) {
            avoidRedirections();
        }
    };

    // Function to python
    window.insertMarkdown = function(md) {
        document.getElementById('content').innerHTML += marked.parse(md);
        // Apply syntax highlighting to all code blocks
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        // Avoid redirects within the embedded browser
        if (!window.embeddedRedirection) {
            avoidRedirections();
        }
    };

    // Function to python
    window.clearMarkdown = function() {
        document.getElementById('content').innerHTML = '';
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