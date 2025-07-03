# IGT

**IGT** (Information Gathering Toolkit) is a flexible, modular tool for discovering user profiles across various platforms. It is designed for OSINT, research, and reconnaissance purposes.

---

**Developer:** [zerosocialcode](https://github.com/zerosocialcode)  
**Contact:** zerosocialcode@gmail.com

---

## Quick Start

```sh
git clone https://github.com/zerosocialcode/IGT.git
cd IGT
```

## Features

- **Scan for usernames across multiple platforms** (social networks, forums, etc.)
- **Add custom platforms** easily via the CLI, no code editing required
- **Choose specific platforms to scan** or scan all at once
- **Asynchronous, fast scanning** with concurrency control
- **HTML report output** with statistics and clickable profile links
- **Graceful exit and friendly CLI**
- **Modular codebase** for easy extension and maintenance

## Installation

1. Install required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
    - Requirements: `aiohttp`, `rich`

2. (Optional) Create a `plt.json` file with your starting platforms, or add them using the CLI.

## Usage

### Adding a New Platform

Add a new platform (e.g., GitHub) for future scans:
```sh
python main.py --add-platform "github" --url "https://github.com/{}" --validation "Not Found"
```
- Use `{}` in the URL for where the username will be inserted.
- `--validation` is optional; it's a snippet of text that indicates a user was **not found**.

### Running a Scan

1. Launch the tool:
    ```sh
    python main.py
    ```

2. Follow the prompts:
   - Enter username(s) (comma/space separated; leave blank for `admin`)
   - Enter platform(s) (comma separated, or leave blank for all)

3. After completion:
    - An HTML report is generated in the `results/` directory.
    - Summary statistics are displayed in the terminal.

### Example: Scan a Single Platform

```sh
python main.py
# Enter username(s): johndoe
# Enter platform(s): github
```

## Platform Configuration (`plt.json`)

Platforms are stored in `plt.json`. Example entry:
```json
[
  {
    "name": "github",
    "url": "https://github.com/{}",
    "validation": { "text_absent": "Not Found" }
  }
]
```
You can manage this file manually, but the CLI is recommended.

## Output

- HTML report in `results/`, with pie chart and clickable profile links.
- Error log in `results/errors.log` for troubleshooting.

## Extending/Developing

- **Modular codebase:** logic split into `main.py`, `scan.py`, `platforms.py`, `utils.py`.
- Easily add new features (proxy support, rate limiting, etc.)

## License

This project is for educational and research purposes only.

---

**Thank you for using IGT Toolkit!**
