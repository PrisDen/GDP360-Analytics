#!/usr/bin/env python3
"""
GDP360 Analytics Setup Script
A comprehensive data analysis platform for global economic data.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gdp360-analytics",
    version="1.0.0",
    author="Priyansh Nandwana",
    author_email="priyansh.nandwana@example.com",
    description="A comprehensive data analysis platform for global economic data from 1975-2024",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PrisDen/GDP360-Analytics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Database",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "viz": [
            "plotly>=5.0.0",
            "dash>=2.0.0",
            "streamlit>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gdp360-etl=gdp360_analytics.etl_pipeline:main",
            "gdp360-analysis=gdp360_analytics.data_analysis:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gdp360_analytics": [
            "raw data/*.csv",
            "*.sql",
            "*.md",
        ],
    },
    keywords="economics, gdp, data-analysis, visualization, sqlite, pandas",
    project_urls={
        "Bug Reports": "https://github.com/PrisDen/GDP360-Analytics/issues",
        "Source": "https://github.com/PrisDen/GDP360-Analytics",
        "Documentation": "https://github.com/PrisDen/GDP360-Analytics/blob/main/DOCUMENTATION.md",
    },
)
