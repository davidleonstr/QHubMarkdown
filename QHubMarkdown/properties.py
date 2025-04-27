from .utils.read import readFileContent
import os

# Location paths of dependency files expressed in a dictionary
libs = {
    'folders': {
        'libs': 'libs', # Expressed name: raw name of the folder
        'js': 'js',
        'css': 'css'
    },
    'dependencies': {
        'js': {
            'marked': 'marked.min.js', # Expressed name: raw name of the file
            'highlight': 'highlight.min.js',
        },
        'css': {
            'highlight.light': 'highlight.light.min.css',
            'highlight.dark': 'highlight.dark.min.css'
        }
        
    }
}

# Location paths of resources files expressed in a dictionary
resources = {
    'folder': 'resources', # Expressed name: raw name of the folder
    'files': {
        'html': 'QHubMarkdown.html', # Expressed name: raw name of the file
        'css.light': 'css/QHubMarkdown.light.css',
        'css.dark': 'css/QHubMarkdown.dark.css',
        'js': 'QHubMarkdown.js'
    }
}

# Current directory
currentDir = os.path.dirname(os.path.abspath(__file__))

# Dependency file content
markedJS = readFileContent(
    os.path.join(
        currentDir, 
        libs['folders']['libs'], 
        libs['folders']['js'], 
        libs['dependencies']['js']['marked'] # Name
    )
)

# Dependency file content
highlightJS = readFileContent(
    os.path.join(
        currentDir, 
        libs['folders']['libs'], 
        libs['folders']['js'], 
        libs['dependencies']['js']['highlight'] # Name
    )
)

# Contents of the resource file
customJS = readFileContent(
    os.path.join(
        currentDir, 
        resources['folder'], 
        resources['files']['js'] # Name
    )
)

# Contents of the resource file
htmlTemplate = readFileContent(
    os.path.join(
        currentDir, 
        resources['folder'], 
        resources['files']['html'] # Name
    )
)

# All style themes
THEMES = {
    'custom': { # Customizable
        'dark': resources['files']['css.dark'],
        'light': resources['files']['css.light']
    },
    'dependence': { # Non-customizable because they are embedded code highlighting dependencies
        'dark': libs['dependencies']['css']['highlight.dark'],
        'light': libs['dependencies']['css']['highlight.light']   
    }
}

def QHubMarkdownHTML(theme: str, customCSS: str = None) -> str:
    """
    Create the complete HTML with embedded dependencies.

    Args:
        theme (str): Default GitHub theme ('dark', 'light').
        customCSS (str, optional): External style that will replace the component style. Default is None.
    """
    if customCSS is None:
        # External custom style
        css = readFileContent(
            os.path.join(
                currentDir, 
                resources['folder'], 
                THEMES['custom'][theme]
            )
        )
    else:
        css = customCSS

    # Chosen style theme
    dependence = readFileContent(
        os.path.join(
            currentDir, 
            libs['folders']['libs'], 
            libs['folders']['css'], 
            THEMES['dependence'][theme]
        )
    )

    # HTML template texts are replaced
    QHubMarkdownHTML = htmlTemplate\
        .replace(r'.custom_css{filter:file;}', css)\
        .replace(r'.highlight_css{filter:file;}', dependence)\
        .replace(r'{marked_js}', markedJS)\
        .replace(r'{highlight_js}', highlightJS)\
        .replace(r'{custom_js}', customJS)
    
    return QHubMarkdownHTML