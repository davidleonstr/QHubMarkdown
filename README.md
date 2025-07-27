# QHubMarkdown

**QHubMarkdown** is a component **renders Markdown** text in a `PyQt/PySide` application, leveraging `PyQtWebEngine` for rendering and utilizing the *highlight.min.js* and *marked.min.js* libraries for **syntax highlighting** and **Markdown** parsing, respectively. 

It also **incorporates** the **styling** used by `GitHub's` Markdown renderer, ensuring a familiar and consistent look and feel for the rendered content.

The widget is designed to **simplify** the rendering of **Markdown** content with **embedded code** in `PyQt/PySide` applications. Its familiar style, resembling `GitHub's` Markdown renderer, makes it easy to integrate into applications with similar requirements.

---

## Key Features

- **Markdown rendering**:
  - Seamlessly display Markdown content in your `PyQt/PySide` applications.
  - Supports embedded code and custom formatting.

- **Code highlighting**:
  - Leverages *highlight.js* for **automatic syntax highlighting** in code blocks.
  - Supports a wide range of programming languages.

- **Themes**:
  - Built-in support for light and dark themes, mimicking `GitHub's` style.
  - Customizable styling to match your application's look and feel.

- **WebChannel communication**:
  - Bidirectional communication between Python and JavaScript.
  - Retrieve the current markdown text from the rendered content.
  - Real-time data exchange for interactive applications.

---

## Installation

> **Requirements:**
> - Python 3.11.3 or higher is required.
> - It is recommended to use a virtual environment (such as `venv`, `virtualenv`, or `conda`) to avoid dependency conflicts.

```bash
# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

You can install **QHubMarkdown** directly from the source code by cloning the repository:

```bash
git clone https://github.com/davidleonstr/QHubMarkdown.git
cd QHubMarkdown
pip install .
```

Or using git + pip to install **QHubMarkdown** using the link to the repository:

```bash
pip install git+https://github.com/davidleonstr/QHubMarkdown.git
```

**For development:**
```bash
git clone https://github.com/davidleonstr/QHubMarkdown.git
cd QHubMarkdown
pip install -e .
```

## Usage

To integrate the **QHubMarkdown** widget into your `PyQt/PySide` application and render Markdown content, follow the example below:

```python
from qtpy.QtWidgets import QApplication, QMainWindow
from QHubMarkdown import QHubMarkdown
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create an instance of QHubMarkdown with a dark theme (default theme)
        self.markdown = QHubMarkdown(theme="dark")
        
        # Initial markdown content to display
        initialText = "# Hello 👋\nThis is a simple markdown renderer in PyQt/PySide."
        
        # Insert the markdown content into the widget
        self.markdown.insertMarkdown(initialText)
        
        # Set the widget as the central widget of the main window
        self.setCentralWidget(self.markdown)
        
        self.setWindowTitle("Markdown Viewer")
        self.resize(800, 600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
```

## Screenshots

![QHubMarkdown in action](https://drive.google.com/uc?id=1p8vNegqiVqY2j8m62AJ7LihmpErFTn3k)

## How to run the examples

<details>
<summary>Click to expand instructions for running the examples in <code>examples/</code>.</summary>

You can find usage examples in the [`examples`](./examples) folder.

To run an example, use the following command in your terminal from the project root:

```bash
python examples/widget_display.py
```

Or try the Markdown editor example:

```bash
python examples/markdown_editor.py
```

**Example descriptions:**
- <code>widget_display.py</code>: Shows how to render Markdown in a PyQt/PySide window.
- <code>markdown_editor.py</code>: Example of an interactive Markdown editor with WebChannel support.

</details>
