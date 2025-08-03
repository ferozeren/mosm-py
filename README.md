# mosm-py: Weather & Air Quality CLI

A lightweight Python CLI tool for fetching real-time weather and air quality data for any location. Powered by WeatherAPI and managed with uv for fast dependency management and isolated Python environments.

## 🚀 Quick Start

Get started with mosm-py in just a few steps:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

   Install uv for efficient dependency management. Follow the official installation guide if you haven't set it up yet.

2. Clone the Repository

   ```bash
   git clone https://github.com/ferozeren/mosm-py.git
   cd mosm-py
   ```

3. Set Up Your API Key

   Sign up for a free API key at WeatherAPI. Add it to a .env file in the project root or configure it directly in main.py.

   **Option 1: Using a .env file**

   Create a .env file in the project root:

   ```env
   WEATHER_API_KEY=your_api_key_here
   ```

   **Option 2: Using main.py**

   Set the user_api_key variable in main.py:

   ```python
   user_api_key = "your_api_key_here" # Leave empty to load from .env
   ```

4. Run the App

   Launch the app using uv:

   ```bash
   uv run main.py
   ```

## 📸 Screenshots

<img width="1419" height="477" alt="New_York" src="https://github.com/user-attachments/assets/1063f3b0-c441-4bca-9063-1efa0b6b7648" />

## ✨ Features

- Retrieve real-time weather data (temperature, humidity, wind speed, etc.).
- Access air quality information (AQI, pollutants, etc.).
- Simple and user-friendly CLI interface.
- Powered by uv for fast and reliable dependency management.

## 🛠️ Requirements

- Python 3.8 or higher
- uv (recommended for dependency management)
- A valid WeatherAPI key

## 📝 Usage

Run the CLI with a location:

```bash
uv run main.py
[location]
```

Example:

```bash
uv run main.py
"New York"
```

## 🤝 Contributing

Contributions are welcome! To contribute:

- Fork the repository.
- Create a new branch for your changes.
- Submit a pull request with a clear description of your updates.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
