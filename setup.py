from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gmail-ai-assistant",
    version="1.0.0",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Assistente de IA para Gmail e Google Calendar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/gmail-ai-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "google-generativeai",
        "rich",
        "click",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "gmail-assistant=gmail_ai_assistant.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gmail_ai_assistant": ["*.json", "*.yaml", "*.yml"],
    },
) 