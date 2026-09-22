# Teardown Steam Workshop Mod Transfer

Transfer all 358 subscribed Teardown (AppID `1167630`) Workshop mods from
one Steam account to another – fully automatically, without opening
hundreds of browser tabs and without needing to create a Workshop Collection.

Two approaches are provided:

| Approach | File | Automation | Requirements |
|---|---|---|---|
| **Fully automatic** (recommended) | `subscribe_mods.py` | Zero clicks | Python 3.8+, `requests` |
| **Semi-automatic** | `subscribe_mods.ps1` / `subscribe_mods.bat` | One click per mod | Windows PowerShell |

---

## Option A – Fully Automatic (Python)

### 1. Install Python and the dependency

> **Important:** Run all commands **from inside the `teardown-workshop-transfer` folder**.
> Open a Command Prompt in that folder (e.g. Shift + right-click → "Open command window here")
> or navigate there first:
>
> ```cmd
> cd C:\path\to\scripts\teardown-workshop-transfer
> pip install -r requirements.txt
> ```

### 2. Get your Steam session cookies

1. Open **https://steamcommunity.com** in any browser (not `store.steampowered.com`).
2. Log in with your **second** Steam account.
3. Press **F12** → **Application** tab → **Cookies** →
   `https://steamcommunity.com`.
4. Copy the values of these two cookies:
   - `sessionid` — looks like `193b8180e9e30ad5e9f8f1e8` (hex string)
   - `steamLoginSecure` — starts with your SteamID followed by `%7C%7C` or `||`,
     then a long JWT token

> **Note:** `steamLoginSecure` will look like
> `76561198000000000%7C%7CeyAidHlwIjogIkpXVCIs...`
> The `%7C%7C` characters are URL-encoded `||` separators — paste the value
> **exactly as shown** in the browser.  The script URL-decodes it automatically.

> **Tip:** In Chrome/Edge the cookies are under
> *Application → Storage → Cookies*.  In Firefox they are under
> *Storage → Cookies*.

### 3. Run the script

Make sure you are still in the `teardown-workshop-transfer` folder, then:

```cmd
python subscribe_mods.py --session-id YOUR_SESSION_ID --steam-login-secure YOUR_STEAM_LOGIN_SECURE
```

Optional flags:

| Flag | Default | Description |
|---|---|---|
| `--delay SECONDS` | `2` | Pause between each subscription request |
| `--dry-run` | — | Print all mod URLs without subscribing |

**Example with 3-second delay:**

```cmd
python subscribe_mods.py --session-id abc123 --steam-login-secure 76561198000000000%7C... --delay 3
```

**Dry-run (just list the mods):**

```cmd
python subscribe_mods.py --session-id x --steam-login-secure x --dry-run
```

The script will print progress for each of the 358 mods:

```
============================================================
  Teardown Steam Workshop Mod Subscriber
  Total mods: 358
============================================================

[  1/358] Mod 2399638522 ... OK
[  2/358] Mod 2400310320 ... OK
...
[358/358] Mod 3673109516 ... OK

============================================================
  Done!  Subscribed: 358  |  Failed: 0
============================================================
```

---

## Option B – Semi-Automatic (PowerShell / Batch)

This opens each Workshop page **inside the Steam client browser**, one at a
time with a configurable delay.  You need to click **Subscribe** on each page.

### Using the batch file (double-click)

1. Make sure **Steam is running** and you are logged in with your second account.
2. Double-click `subscribe_mods.bat`.
3. Press **Enter** to start.
4. Click **Subscribe** on each page as it opens.

### Using PowerShell directly

```powershell
.\subscribe_mods.ps1
# or with a custom delay:
.\subscribe_mods.ps1 -DelaySeconds 5
```

If PowerShell blocks execution, run this once in an elevated shell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Mod list

The mod IDs embedded in both scripts correspond to these local workshop paths:

```
D:\SteamLibrary\steamapps\workshop\content\1167630\<MOD_ID>
```

358 mods for **Teardown** (AppID `1167630`) are included.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `No such file or directory: 'requirements.txt'` or `can't open file '...\subscribe_mods.py'` | You ran the command from the wrong folder.  `cd` into `teardown-workshop-transfer` first. |
| `400 Bad Request` errors | Your cookies were copied from the wrong site.  Use **https://steamcommunity.com** (not the store) and make sure you are logged in with your second account. |
| `FAILED` responses with API result code | Your session may have expired.  Log out, log back in to steamcommunity.com, and copy fresh cookies. |
| `steamLoginSecure does not contain '||'` | The cookie value was truncated.  Copy the full value — it should end with a base64 JWT string after `%7C%7C`. |
| Steam doesn't open mod pages (PowerShell) | Make sure Steam is running and logged in with your second account. |
| PowerShell says "cannot be loaded because running scripts is disabled" | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell as Administrator. |
| Python not found | Download from https://www.python.org/downloads/ and ensure "Add to PATH" is checked during install. |
