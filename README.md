# ✨ IGT: Information Gathering Toolkit

**IGT** is a high-speed, asynchronous toolkit for rapid username reconnaissance and digital investigations. Built for OSINT, cybersecurity, and threat intelligence workflows, IGT offers a seamless CLI experience and actionable insights—all at lightning speed.

---

## ⭐ Highlights

- **Smart Username Variations:**  
  Generates 100+ intelligent username permutations (leet speak, affixes, separators, numeric patterns, and more).

- **Multi-Platform Coverage:**  
  Scan across major networks—Facebook, Instagram, Twitter/X, Snapchat, Telegram, TikTok, Threads, and more.

- **Fast, Asynchronous Scanning:**  
  Uses `asyncio` and `aiohttp` for concurrent HTTP requests—designed for efficiency.

- **Modern CLI Experience:**  
  Progress bars, live spinners, and summary tables, powered by the `rich` library for a refined terminal interface.

- **Professional Reports:**  
  Standalone HTML reports with interactive charts and detailed breakdowns.

- **Comprehensive Error Logging:**  
  All HTTP and parsing errors are logged—non-fatal errors never break the scan.

---

## ⚙️ Requirements

- Python **3.8+**
- Basic Python knowledge

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zerosocialcode/IGT.git
   cd IGT
   ```

2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Quick Start

```bash
python3 igt.py
```
- **Prompt:** Enter the base username (e.g., `johndoe`)
- **Process:** IGT generates intelligent variations, scans all platforms in parallel, and displays real-time progress.
- **Result:** Interactive HTML report in the `results/` directory.

---

## ⚙️ Configuration & Customization

### Platform Matrix

Edit or extend platforms in `plt.json`:
```json
[
  {
    "name": "twitter",
    "url": "https://twitter.com/{}",
    "validation": { "text_absent": "Sorry, that page doesn’t exist!" }
  },
  {
    "name": "instagram",
    "url": "https://www.instagram.com/{}/",
    "validation": { "absent": "Sorry, this page isn’t available." }
  }
  // ...add your own!
]
```

### User Agents

Rotate headers by customizing the `USER_AGENTS` list in `IGT.py` to help avoid rate-limiting.

### Performance Tuning

Adjust `DEFAULT_CONCURRENCY` in `IGT.py` for optimal speed vs. platform rate limits.

### Other Customizations

- **Platforms:** Add or update entries in `plt.json`
- **Variation Logic:** Tweak `generate_variations()` for custom patterns
- **Report Design:** Modify HTML/CSS or Chart.js in the report generator

---

## 📈 Output & Reporting

- **results/**: All scans saved as interactive HTML reports
- **errors.log**: Comprehensive error and exception logs
- **<username>_scan_<timestamp>.html**: Summary reports with interactive charts

---

## 🛡️ Reliability

- All errors are non-blocking & logged to `results/errors.log`
- The scan never halts on routine failures

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch (`feature/your-feature`)
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

Licensed under the MIT License. See [LICENSE](LICENSE).

---

> Built with Python by [zerosocialcode](https://github.com/zerosocialcode)
