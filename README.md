# TTS Spanish Jank Normalizer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](./CONTRIBUTING.md)

A robust Python library designed to preprocess and normalize complex Spanish text, making it perfectly digestible for even the most 'janky' Text-to-Speech (TTS) engines.

## The Motivation

Standard Text-to-Speech (TTS) engines are powerful, but they often fail when faced with the nuances of written Spanish. They mispronounce abbreviations, stumble over numbers, and incorrectly read symbols, leading to unnatural and unprofessional-sounding audio.

This project was born out of a practical need to generate high-quality, professional-sounding audio for AI-driven news summary videos at **[noticiasresumidas.com](https://noticiasresumidas.com)**. By normalizing the text *before* sending it to the TTS engine, we ensure a clean, consistent, and human-like audio output, dramatically improving the quality of our content.

This "jank normalizer" is the bridge between raw, complex text and a flawless audio experience.

## Key Features

The library transforms a wide variety of problematic patterns into simple, readable text.

| Feature | Before Normalization | After Normalization |
| :--- | :--- | :--- |
| **Abbreviations** | `El Sr. Pérez y la Dra. López` | `El señor Pérez y la doctora López` |
| **Acronyms** | `Según la OMS y la UE...` | `Según la O, M, S y la U, E...` |
| **Complex Numbers** | `Costó 1.250.000,75 €` | `Costó un millón doscientos cincuenta mil coma setenta y cinco euros` |
| **Ordinals** | `La 1ª planta, 3er piso` | `La primera planta, tercer piso` |
| **Roman Numerals** | `El Rey Felipe VI en el Siglo XXI` | `El Rey Felipe sexto en el Siglo veintiuno` |
| **Time (24h & 12h)** | `a las 14:30 h y 8:00 p.m.` | `a las catorce y treinta y ocho de la noche` |
| **Units & Symbols** | `80 km/h con un 50% de dto.` | `ochenta kilómetros por hora con un cincuenta por ciento de dto.` |
| **Ranges & Fractions**| `Páginas 20-25; 1/2 del total` | `Páginas veinte a veinticinco; un medio del total` |
| **Contact Info**| `info@test.com / +34 912-34-56`| `info arroba test punto com / más 3 4 9 1 2 3 4 5 6` |

## Installation

The project is structured as a Python package and has one main dependency.

1.  **Install the dependency:**
    ```bash
    pip install num2words
    ```

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/tts_spanish_jank_normalizer.git
    ```

3.  **Use the package:**
    Place the `tts_spanish_jank_normalizer` directory (the one containing the `normalizacion` folder) into your project's root directory. You can then import it directly.

## Quick Start

Using the normalizer is straightforward. Import the main `normalize_text` function and a logger, and you're ready to go.

```python
# Import the public functions from the package
from tts_spanish_jank_normalizer import normalize_text, setup_default_logger

# 1. Set up the logger (this will create a 'normalization.log' file with details)
logger = setup_default_logger()

# 2. Define a complex text string
raw_text = "El 1er informe de la OMS (Capítulo IV) dice que 1/2 de los casos del siglo XX ocurrieron a las 8:00 p.m. Contactar en info@test.com."

# 3. Normalize the text!
normalized_text = normalize_text(raw_text, logger)

# 4. Print the result
print("--- Original Text ---")
print(raw_text)
print("\n--- Normalized for TTS ---")
print(normalized_text)

# The 'normalized_text' is now ready to be sent to your TTS engine.
```

### Expected Output:

```
--- Original Text ---
El 1er informe de la OMS (Capítulo IV) dice que 1/2 de los casos del siglo XX ocurrieron a las 8:00 p.m. Contactar en info@test.com.

--- Normalized for TTS ---
El primer informe de la O, M, S (Capítulo cuarto) dice que un medio de los casos del siglo veinte ocurrieron a las ocho de la noche. Contactar en info arroba test punto com.
```

## The Normalization Pipeline

The library processes text through a carefully ordered pipeline of modules to handle specific patterns without interfering with each other. The execution order is:
1.  Abbreviations (`Sr.`, `Av.`)
2.  Acronyms (`OMS`)
3.  Identifiers (`info@test.com`, phone numbers)
4.  Time Formats (`14:30 h`, `8:00 p.m.`)
5.  Ordinals (`1º`, `2ª`)
6.  Roman Numerals (`Siglo XXI`)
7.  Ranges & Fractions (`20-25`, `3/4`)
8.  Units & Symbols (`km/h`, `%`, `€`)
9.  General Numbers (any remaining digits)

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

Don't forget to give the project a star! Thanks again!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
