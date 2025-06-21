# IGT: Information Gathering Toolkit

**IGT** is a high-speed, asynchronous toolkit for scanning social media usernames and their smart variations across multiple platforms. Designed for OSINT and digital investigations, IGT leverages Python's async capabilities for rapid, concurrent scanning, beautiful CLI output, and rich HTML reporting.

---

## 🚀 Features

- **Smart Username Variations:** Generates 100+ permutations including leet speak, prefixes, suffixes, numbers, and separators.
- **Multi-Platform Support:** Scan up to 8 major platforms—Facebook, Instagram, Twitter/X, Snapchat, Telegram, TikTok, Threads, and more.
- **Async & Concurrent:** Harnesses asyncio and aiohttp for concurrent HTTP requests, with user-configurable concurrency.
- **Rich CLI:** Progress bars, spinners, and summary tables via the `rich` library for a polished terminal experience.
- **HTML Report:** Generates standalone HTML files with real-time pie charts and detailed results.
- **Error Logging:** All HTTP and parsing errors are logged for review; non-fatal errors won’t halt scanning.

---

## ⚙️ Prerequisites

- Python 3.8+
- Basic Python knowledge

---

<<<<<<< HEAD
## 🛠️ Installation
=======
🛠️ Installation

1. Clone the Repository:
```
git clone https://github.com/zerosocialcode/IGT.git
cd IGT
```

2. Create & Activate Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

3. Install Dependencies:
```
pip install -r requirements.txt
```



---

🔧 Configuration

1. Platform Definitions: Edit or create plt.json based on provided sample:
```
[
  {
    "name": "twitter",
    "url": "https://twitter.com/{}",
    "validation": { "text_absent": "Sorry, that page doesn\u2019t exist!" }
  },
  {
    "name": "instagram",
    "url": "https://www.instagram.com/{}/",
    "validation": { "absent": "Sorry, this page isn\u2019t available." }
  }
  // ... add or update platforms
]
```

2. User Agents: Customize USER_AGENTS in IGT.py to rotate request headers.


3. Concurrency: Adjust DEFAULT_CONCURRENCY to optimize performance vs. rate limits.




---

▶️ Usage

Run the scanner:
```
python3 igt.py
```
Prompt: Enter the base username (e.g., johndoe).

Process: The script generates variations, scans each platform concurrently, and displays a live progress bar.

📂 Outputs

results/ directory: Saves in a html format file.

errors.log: Logged exceptions and errors.

<username>_scan_<timestamp>.html: Interactive HTML report with charts and details.

---

🛠️ Customization

Adding Platforms: Add JSON entries in plt.json.

Variation Rules: Modify generate_variations() for custom patterns.

Report Styling: Tweak CSS or Chart.js config in save_html().

---

🐞 Error Handling & Logs

All HTTP and parsing errors are appended to results/errors.log.

Non-fatal errors won’t stop the scan; they’ll be recorded and skipped.

---

🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo


2. Create a feature branch feature/awesome-feature


3. Commit your changes


4. Open a Pull Request


---

📜 License

This project is licensed under the MIT License. See LICENSE for details.


---

> Built with ❤️ and Python by zerosocialcode.


>>>>>>> 476ebf6 (Updated README with new details)

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/zerosocialcode/IGT.git
   cd IGT