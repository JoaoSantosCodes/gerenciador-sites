from setuptools import setup, find_packages

setup(
    name="gerenciador-sites",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cryptography>=41.0.0",
        "bcrypt>=4.0.1",
        "Flask>=3.0.0",
        "SQLAlchemy>=2.0.0",
        "pycryptodome>=3.19.0",
        "python-dotenv>=1.0.0",
        "pytest>=7.4.0",
        "black>=23.0.0",
        "flake8>=6.1.0",
        "beautifulsoup4"
    ],
    python_requires=">=3.8",
) 