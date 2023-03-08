import setuptools
  
with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()
  
setuptools.setup(
    name="cmd_chat",
    version="1.0",
    author="dinosaurtirex",
    author_email="sneakybeaky18@gmail.com",
    packages=["cmd_chat"],
    description="Secured console chat with RSA & Fernet",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/dinosaurtirex/cmd-chat",
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        "sanic",
        "requests",
        "rsa",
        "cryptography",
        "colorama",
        "pydantic",
        "websocket-client"
    ]
)