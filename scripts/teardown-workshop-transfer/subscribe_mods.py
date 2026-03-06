#!/usr/bin/env python3
"""
Steam Workshop Mod Subscriber for Teardown (AppID: 1167630)

Automatically subscribes to all listed Teardown Workshop mods on the
Steam account that is currently logged in via your browser session.

Usage
-----
  python subscribe_mods.py --session-id SESSION_ID --steam-login-secure SECURE_VALUE

How to obtain your Steam session cookies
-----------------------------------------
  1. Open https://steamcommunity.com in your browser and log in with your SECOND account.
  2. Press F12 to open Developer Tools, then go to:
       Application → Cookies → https://steamcommunity.com
  3. Copy the values of these two cookies:
       - sessionid     (e.g. 193b8180e9e30ad5e9f8f1e8)
       - steamLoginSecure  (starts with your SteamID, e.g. 765611990...%7C%7CeyA...)
  4. Paste the values as-is; URL-encoded characters like %7C%7C are handled automatically.

Options
-------
  --session-id          Steam 'sessionid' cookie value (required)
  --steam-login-secure  Steam 'steamLoginSecure' cookie value (required)
  --delay               Seconds to wait between subscriptions (default: 2)
  --dry-run             List all mod IDs/URLs without actually subscribing
"""

import sys
import time
import argparse
import urllib.parse
import requests

APP_ID = "1167630"  # Teardown

# All 358 Teardown Workshop mod IDs to subscribe to.
MOD_IDS = [
    "2399638522", "2400310320", "2400346027", "2400433407", "2400731319",
    "2400745103", "2400974910", "2400975518", "2401575709", "2401576949",
    "2401577403", "2401589688", "2401590758", "2401591426", "2401591811",
    "2401593417", "2401593768", "2401871202", "2401871551", "2401871948",
    "2401872336", "2401872536", "2401872753", "2401872968", "2405694178",
    "2406955331", "2408046525", "2410585832", "2412621869", "2414356052",
    "2414735699", "2414735882", "2414836891", "2414851441", "2415143972",
    "2415158477", "2415637896", "2415643616", "2419814408", "2420362691",
    "2423986361", "2428675434", "2429597912", "2429708963", "2430354051",
    "2430961153", "2437049563", "2446494619", "2453693772", "2463502233",
    "2465001487", "2467373190", "2480490943", "2480612500", "2485433489",
    "2488185625", "2497213038", "2498343049", "2500181730", "2505500526",
    "2511660133", "2512537986", "2514178072", "2525610233", "2526115498",
    "2536589821", "2537399300", "2538651503", "2539026789", "2542995707",
    "2547915810", "2550212862", "2559081519", "2564400770", "2567560405",
    "2580322132", "2594544248", "2597745035", "2598610013", "2602821614",
    "2606695330", "2607739989", "2609031608", "2614499023", "2614697784",
    "2616379809", "2617054592", "2617698716", "2621950566", "2625710852",
    "2630309389", "2631642003", "2632751249", "2632935455", "2639750110",
    "2651225287", "2663552077", "2668505408", "2674819082", "2676258508",
    "2678285559", "2682043380", "2682688380", "2686424606", "2686729186",
    "2689140429", "2691646893", "2691792518", "2713320687", "2716274706",
    "2728957413", "2729602554", "2756340385", "2766504354", "2771353907",
    "2771751543", "2774292557", "2775837358", "2778203662", "2778235968",
    "2779117114", "2779697403", "2779765232", "2781126173", "2781805965",
    "2782336916", "2782381274", "2783676899", "2789549013", "2797610758",
    "2798225284", "2800184096", "2801293186", "2801625356", "2803129277",
    "2804935262", "2805838137", "2807634204", "2807732862", "2807752513",
    "2811441327", "2811441413", "2813414857", "2822564433", "2825097759",
    "2826875208", "2827040867", "2829215554", "2832958716", "2834864515",
    "2835441696", "2836994015", "2838132117", "2839355350", "2840497593",
    "2843815456", "2848237963", "2849020760", "2851115805", "2854339342",
    "2854539326", "2856313468", "2860100708", "2862047863", "2863781508",
    "2867003293", "2872005797", "2877387699", "2883178204", "2883257654",
    "2883257690", "2883259047", "2885060440", "2888332434", "2889602163",
    "2893255767", "2893951147", "2895949873", "2898332095", "2902815293",
    "2905386230", "2906369984", "2914894991", "2916794806", "2919533122",
    "2921439149", "2922009802", "2932118143", "2932177081", "2933294498",
    "2935746653", "2937827747", "2953615853", "2981516505", "2990976650",
    "2994616319", "2995483003", "3002996975", "3004952393", "3005988296",
    "3021153052", "3028163018", "3041246583", "3043466411", "3046923786",
    "3084655695", "3089285933", "3114561159", "3121148747", "3125053767",
    "3128555334", "3137437703", "3148138736", "3148143301", "3150989946",
    "3151710846", "3165358166", "3173859813", "3183933526", "3183943578",
    "3199019196", "3209546457", "3219470184", "3254618944", "3255577176",
    "3260706688", "3288587192", "3289269367", "3291524296", "3294073011",
    "3297141296", "3301544536", "3302127939", "3304564578", "3305002216",
    "3307042743", "3310501971", "3311625322", "3314869918", "3321679150",
    "3323801242", "3324157941", "3325882246", "3330426273", "3330518512",
    "3340357504", "3347196228", "3348340556", "3349075962", "3349820251",
    "3352195923", "3354647772", "3357324612", "3362155617", "3379664555",
    "3386469510", "3390618056", "3391669081", "3392531141", "3400905136",
    "3407159262", "3418558763", "3422267160", "3430510022", "3432643239",
    "3437299817", "3449069614", "3458623567", "3459643136", "3466371185",
    "3467223461", "3477397847", "3482237945", "3485769450", "3488266245",
    "3490932069", "3497952769", "3507369528", "3507679500", "3512351066",
    "3512683482", "3520240647", "3539765430", "3541730926", "3552550966",
    "3560808573", "3563619256", "3585845450", "3620875552", "3621598329",
    "3621818416", "3621835738", "3622131440", "3622316486", "3622325648",
    "3622337112", "3622494409", "3622561177", "3622607133", "3622980011",
    "3622995276", "3623069506", "3623102511", "3623129900", "3623223501",
    "3623280942", "3623306657", "3623351152", "3623360646", "3623379559",
    "3623390604", "3623461451", "3623476589", "3623756855", "3623793087",
    "3625052942", "3625277442", "3625284752", "3625485087", "3626117001",
    "3626219284", "3626409416", "3626963081", "3627968698", "3628008974",
    "3628059485", "3628141333", "3628255225", "3628864229", "3629119676",
    "3629237934", "3629456835", "3629505664", "3629654392", "3632322337",
    "3632548813", "3632821615", "3634551685", "3635399720", "3636049807",
    "3636687709", "3636888504", "3637514598", "3639387869", "3640768304",
    "3643554507", "3647839189", "3649052752", "3654319853", "3656400747",
    "3657228189", "3660484241", "3662000095", "3667076645", "3667701976",
    "3667727633", "3670441211", "3673109516",
]

SUBSCRIBE_URL = "https://steamcommunity.com/sharedfiles/subscribe"


def parse_steam_login_secure(raw_value: str) -> tuple[str, str]:
    """
    Parse the steamLoginSecure cookie value into (steam_id, jwt_token).

    The cookie value is either:
      - URL-encoded: 76561199...%7C%7CeyA...   (as copied from browser DevTools)
      - Raw:         76561199...||eyA...
    Both formats are handled automatically.
    """
    decoded = urllib.parse.unquote(raw_value)
    if "||" not in decoded:
        raise ValueError(
            "steamLoginSecure does not contain '||'.  "
            "Make sure you copied the full 'steamLoginSecure' cookie value "
            "from https://steamcommunity.com (not the store)."
        )
    steam_id, jwt_token = decoded.split("||", 1)
    return steam_id.strip(), jwt_token.strip()


def subscribe_to_mod(
    session: requests.Session,
    mod_id: str,
    session_id: str,
) -> bool:
    """Send a subscribe request to Steam Community for a single Workshop mod.

    Uses steamcommunity.com/sharedfiles/subscribe, which authenticates via the
    session cookies (sessionid + steamLoginSecure) already attached to the
    session object.  No API key or JWT parameter is required.
    """
    data = {
        "sessionid": session_id,
        "id": mod_id,
        "appid": APP_ID,
    }
    try:
        resp = session.post(
            SUBSCRIBE_URL,
            data=data,
            timeout=15,
        )
        resp.raise_for_status()
        result = resp.json()
        # Community endpoint returns {"success": 1} on success.
        # success=8 (EResult::AlreadySubscribed) is also acceptable.
        code = result.get("success", -1)
        if code in (1, 8):
            return True
        print(f"  API result code {code}", file=sys.stderr)
        return False
    except requests.exceptions.HTTPError as exc:
        body = ""
        if exc.response is not None:
            body = exc.response.text[:200]
        status = exc.response.status_code if exc.response is not None else "?"
        print(f"  HTTP {status} error: {body}", file=sys.stderr)
        return False
    except requests.exceptions.RequestException as exc:
        print(f"  Request error: {exc}", file=sys.stderr)
        return False
    except ValueError:
        print("  Unexpected response (not JSON)", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automatically subscribe to all listed Teardown Workshop mods.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--session-id",
        default=None,
        metavar="SESSION_ID",
        help="Value of the 'sessionid' cookie from steamcommunity.com",
    )
    parser.add_argument(
        "--steam-login-secure",
        default=None,
        metavar="VALUE",
        help="Value of the 'steamLoginSecure' cookie from steamcommunity.com",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help="Delay in seconds between each subscription request (default: 2)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print mod IDs and URLs without actually subscribing",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Teardown Steam Workshop Mod Subscriber")
    print(f"  Total mods: {len(MOD_IDS)}")
    print("=" * 60)
    print()

    if args.dry_run:
        print("DRY-RUN MODE – no subscriptions will be made.\n")
        for mod_id in MOD_IDS:
            print(f"  https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}")
        print(f"\n{len(MOD_IDS)} mod URLs listed.")
        return

    # ── Interactive prompts (used when launched via RUN_ME.bat or with no flags) ──
    if args.session_id is None or args.steam_login_secure is None:
        print("  How to get your Steam cookies:")
        print("  1. Open https://steamcommunity.com in your browser.")
        print("  2. Log in with your SECOND Steam account.")
        print("  3. Press F12 → Application tab → Cookies →")
        print("       https://steamcommunity.com")
        print("  4. Copy and paste the two values requested below.")
        print()

    if args.session_id is None:
        args.session_id = input("  Paste 'sessionid' value : ").strip()

    if args.steam_login_secure is None:
        print()
        print("  The 'steamLoginSecure' value starts with your SteamID")
        print("  (e.g. 76561198...) followed by %7C%7C and a long JWT.")
        args.steam_login_secure = input("  Paste 'steamLoginSecure' value : ").strip()
        print()

    # ── Validate steamLoginSecure format ──────────────────────────────────────
    # steamLoginSecure format (after URL-decoding): STEAMID||JWT
    try:
        parse_steam_login_secure(args.steam_login_secure)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    # URL-decode the steamLoginSecure value so the cookie is stored correctly.
    decoded_secure = urllib.parse.unquote(args.steam_login_secure)

    print("Make sure you are logged in with your SECOND account in the browser")
    print("before running this script, and that the cookies you provided are")
    print("for that second account.")
    print()
    print(f"Delay between requests : {args.delay}s")
    print()

    session = requests.Session()
    session.cookies.set("sessionid", args.session_id, domain="steamcommunity.com")
    session.cookies.set("steamLoginSecure", decoded_secure, domain="steamcommunity.com")
    session.headers.update(
        {
            "Referer": "https://steamcommunity.com/",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        }
    )

    ok_count = 0
    fail_count = 0
    total = len(MOD_IDS)

    for i, mod_id in enumerate(MOD_IDS, start=1):
        print(f"[{i:>3}/{total}] Mod {mod_id} ... ", end="", flush=True)
        success = subscribe_to_mod(session, mod_id, args.session_id)
        if success:
            print("OK")
            ok_count += 1
        else:
            print("FAILED")
            fail_count += 1

        if i < total:
            time.sleep(args.delay)

    print()
    print("=" * 60)
    print(f"  Done!  Subscribed: {ok_count}  |  Failed: {fail_count}")
    print("=" * 60)

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
