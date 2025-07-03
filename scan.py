import asyncio
import random
import aiohttp
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Mobile; rv:109.0) Gecko/112.0 Firefox/112.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

async def fetch_profile(session, url, headers):
    tries = 2
    for _ in range(tries):
        try:
            async with session.get(url, headers=headers, timeout=20, ssl=False) as resp:
                text = await resp.text(errors="replace")
                return resp.status, text
        except Exception:
            await asyncio.sleep(1)
    return None, None

async def scan_username_on_platform(session, plat, username, semaphore, log_error):
    url = plat["url"].format(username)
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    async with semaphore:
        status, text = await fetch_profile(session, url, headers)
    absent = plat.get("validation", {}).get("text_absent", "") or plat.get("validation", {}).get("absent", "")
    found = False
    try:
        if status == 200 and absent:
            if absent.lower() not in text.lower():
                found = True
        elif status == 200 and not absent:
            found = True
    except Exception as e:
        log_error(f"Error parsing {url}: {e}")
    return {
        "platform": plat["name"],
        "username": username,
        "found": found,
        "url": url
    }

async def scan_all(usernames, platforms, concurrency, log_error, console):
    results = []
    semaphore = asyncio.Semaphore(concurrency)
    total = len(platforms) * len(usernames)
    task_args = []
    for plat in platforms:
        for uname in usernames:
            task_args.append((plat, uname))
    with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TimeElapsedColumn(),
            "•",
            TimeRemainingColumn(),
            console=console,
            transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Scanning...", total=total)
        async with aiohttp.ClientSession() as session:
            tasks = [
                scan_username_on_platform(session, plat, uname, semaphore, log_error)
                for plat, uname in task_args
            ]
            for coro in asyncio.as_completed(tasks):
                res = await coro
                results.append(res)
                progress.update(task, advance=1)
    return results
