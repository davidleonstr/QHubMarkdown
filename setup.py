from setuptools import setup, find_packages

setup(
    name="QHubMarkdown",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "PyQt5-Qt5",
        "PyQt5_sip",
        "PyQtWebEngine",
        "PyQtWebEngine-Qt5",
        "setuptools",
    ],
    description="A PyQt5-based Markdown viewer with syntax highlighting and GitHub-like styling.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="David León",
    author_email="davidalfonsoleoncarmona@gmail.com",
    url="https://github.com/davidleonstr/QWMarkdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.3",
)

# I use Python 3.13.1.