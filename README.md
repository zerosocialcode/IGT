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

## 🛠️ Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/zerosocialcode/IGT.git
   cd IGT