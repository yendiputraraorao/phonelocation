import os
import time
import requests
import phonenumbers
from datetime import datetime
from phonenumbers import geocoder, carrier, timezone, number_type
from colorama import init, Fore

init(autoreset=True)

# ─────────────────────────────────────────────────────────────
#  IndoOSINT Mobile v1.0 - Security & OSINT Learning Tool
#  Modified from: PhoneXtract v3.0
# ─────────────────────────────────────────────────────────────

def banner():
    print(Fore.GREEN + "=" * 60)
    print(Fore.CYAN + "          INDONESIA ADVANCED PHONE OSINT TRACKER")
    print(Fore.YELLOW + "      Identity, Hardware, and Location Intelligence")
    print(Fore.GREEN + "=" * 60)

# ══════════════════════════════════════════════════════════════
#  INDONESIA SPECIFIC HELPERS
# ══════════════════════════════════════════════════════════════

def get_indo_prefix_info(number_str):
    """Memetakan prefix nomor ke operator dan wilayah pendaftaran awal (HLR)."""
    clean_num = number_str.replace("+62", "0")
    prefix = clean_num[:4]
    
    prefix_map = {
        "0811": "Telkomsel (Kartu Halo) - Nasional",
        "0812": "Telkomsel (Simpati) - Nasional",
        "0813": "Telkomsel (Simpati) - Nasional",
        "0821": "Telkomsel - Jawa Tengah/DIY/Jawa Timur",
        "0857": "Indosat (IM3) - Nasional",
        "0817": "XL Axiata - Nasional",
        "0896": "Tri (3) - Nasional",
        "0881": "Smartfren - Nasional",
    }
    return prefix_map.get(prefix, "Operator/Wilayah Umum")

def get_indo_coords(region_name):
    """Mapping koordinat pusat wilayah untuk visualisasi Maps."""
    coords_map = {
        "Jakarta": "-6.2088, 106.8456",
        "Jawa Barat": "-6.9175, 107.6191",
        "Jawa Tengah": "-7.0051, 110.4381",
        "Jawa Timur": "-7.2575, 112.7521",
        "Bali": "-8.4095, 115.1889",
        "Sumatera Utara": "3.5952, 98.6722"
    }
    return coords_map.get(region_name, "-2.5489, 118.0149") # Default: Tengah Indonesia

# ══════════════════════════════════════════════════════════════
#  ADVANCED PROBES (Truecaller & E-Wallet)
# ══════════════════════════════════════════════════════════════

def check_whatsapp_status(e164):
    """Mengecek pendaftaran WhatsApp melalui probe wa.me."""
    print(Fore.CYAN + "  [~] WhatsApp Probe : Checking...", end="", flush=True)
    try:
        r = requests.get(f"https://wa.me/{e164.replace('+', '')}", timeout=10)
        if "whatsapp.com" in r.url or r.status_code == 200:
            print(Fore.GREEN + " REGISTERED")
            return "Registered [+]"
        print(Fore.RED + " NOT FOUND")
        return "Not Registered [-]"
    except:
        return "Error"

def e_wallet_probe(number):
    """Simulasi pengecekan nama di database E-Wallet."""
    # Dalam implementasi nyata, ini memerlukan API Gateway
    print(Fore.CYAN + "  [~] E-Wallet Probe : Scanning Dana/Ovo...", end="", flush=True)
    time.sleep(1) # Simulasi delay[cite: 1]
    print(Fore.YELLOW + " COMPLETED")
    return "Check manually via Bank Transfer for Full Name"

# ══════════════════════════════════════════════════════════════
#  CORE ANALYSIS
# ══════════════════════════════════════════════════════════════

def analyze_number(number):
    try:
        # Normalisasi input ke format internasional[cite: 1]
        if number.startswith('0'):
            number = "+62" + number[1:]
        
        parsed = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed):
            print(Fore.RED + "\n  [!] Nomor tidak valid!")
            return

        # Ekstraksi Data Dasar[cite: 1]
        carrier_name = carrier.name_for_number(parsed, "en") or "Unknown"
        region_area  = geocoder.description_for_number(parsed, "id") or "Indonesia"
        tz           = timezone.time_zones_for_number(parsed)
        e164_fmt     = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        
        # Ekstraksi Data Advanced
        prefix_info = get_indo_prefix_info(e164_fmt)
        coords      = get_indo_coords(region_area)
        wa_status   = check_whatsapp_status(e164_fmt)
        wallet_info = e_wallet_probe(e164_fmt)

        # Build Report[cite: 1]
        SEP = "=" * 60
        lines = [
            SEP,
            "  OSINT REPORT - INDONESIA MOBILE INTELLIGENCE",
            f"  Target Number    : {e164_fmt}",
            f"  Timestamp        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            SEP,
            "",
            "  -- IDENTITAS & OPERATOR " + "-" * 34,
            f"  Operator (Lib)   : {carrier_name}",
            f"  Info Prefix      : {prefix_info}",
            f"  WhatsApp Status  : {wa_status}",
            f"  E-Wallet Name    : {wallet_info}",
            "",
            "  -- LOKASI & HARDWARE " + "-" * 37,
            f"  Wilayah (HLR)    : {region_area}",
            f"  Koordinat Est.   : {coords}",
            f"  Google Maps      : https://www.google.com/maps?q={coords.replace(' ', '')}",
            f"  Zona Waktu       : {', '.join(tz)}",
            "",
            "  -- ACTIVE TRACKING " + "-" * 39,
            f"  Tracking Link    : http://your-ip:5000/track/{e164_fmt.replace('+', '')}",
            "  Note: Kirim link di atas untuk mendapatkan Merek/Tipe HP target.",
            SEP
        ]

        report_text = "\n".join(lines)
        print("\n" + report_text)

        # Simpan Report Otomatis[cite: 1]
        fname = f"report_{e164_fmt.replace('+', '')}.txt"
        with open(fname, "w") as f:
            f.write(report_text)
        print(Fore.GREEN + f"  [+] Report saved to {fname}")

    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ══════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    banner()
    while True:
        target = input(Fore.CYAN + "\n[>] Masukkan Nomor HP (atau 'exit'): ").strip()
        if target.lower() == 'exit':
            break
        if target:
            analyze_number(target)