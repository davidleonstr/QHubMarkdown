from setuptools import setup, find_packages

setup(
    name="QHubMarkdown",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "QtPy",
        "PyQt6-WebEngine",
        "setuptools"
    ],
    description="A PyQt/PySide Markdown viewer with syntax highlighting and GitHub-like styling.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="David León",
    author_email="davidalfonsoleoncarmona@gmail.com",
    url="https://github.com/davidleonstr/QHubMarkdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.3",
)

# I use Python 3.13.1.
