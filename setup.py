from setuptools import setup, find_packages

setup(
    name="reader",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.5.0",
        "python-poppler-qt>=0.24.0",
        "ebooklib>=0.17.1",
        "beautifulsoup4>=4.12.0",
    ],
    entry_points={
        'console_scripts': [
            'reader=src.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A minimalist, full-screen document reader for PDF and ePub files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="pdf, epub, reader, viewer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
) 