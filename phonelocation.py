import os
import time
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type
from colorama import init, Fore

init(autoreset=True)

def banner():
    print(Fore.GREEN + "=" * 60)
    print(Fore.CYAN + "          INDONESIA PHONE OSINT - TRACKER v1.0")
    print(Fore.YELLOW + "      Detect Region, Operator, and Timezone (HLR Data)")
    print(Fore.GREEN + "=" * 60)

def get_indonesia_location(number_str):
    """
    Fungsi khusus untuk memetakan prefix operator Indonesia ke wilayah.
    Data ini berdasarkan alokasi awal nomor (HLR).
    """
    # Contoh subset mapping prefix (Bisa dikembangkan lebih detail)
    prefix_map = {
        "0811": "Telkomsel - Nasional (Kartu Halo)",
        "0812": "Telkomsel - Nasional (Simpati)",
        "0813": "Telkomsel - Nasional (Simpati)",
        "0821": "Telkomsel - Jawa Tengah/DIY/Jawa Timur",
        "0822": "Telkomsel - Loop (Nasional)",
        "0852": "Telkomsel - AS (Sumatera/Sulawesi)",
        "0814": "Indosat - Broadband M2",
        "0815": "Indosat - Matrix/Mentari",
        "0816": "Indosat - Matrix/Mentari",
        "0857": "Indosat - IM3 (Nasional)",
        "0817": "XL Axiata - Nasional",
        "0818": "XL Axiata - Nasional",
        "0819": "XL Axiata - Nasional",
        "0878": "XL Axiata - Nasional",
        "0896": "Tri (3) - Nasional",
        "0899": "Tri (3) - Nasional",
        "0881": "Smartfren - Nasional",
        "0882": "Smartfren - Nasional",
    }
    
    # Normalisasi input ke format 08xx
    clean_num = number_str.replace("+62", "0")
    prefix = clean_num[:4]
    
    return prefix_map.get(prefix, "Wilayah/Operator tidak spesifik di database prefix")

def analyze_indonesia_number(num_input):
    try:
        # Menambahkan +62 jika user lupa
        if num_input.startswith('0'):
            num_input = "+62" + num_input[1:]
        elif not num_input.startswith('+'):
            num_input = "+" + num_input

        parsed = phonenumbers.parse(num_input, None)
        
        if not phonenumbers.is_valid_number(parsed):
            print(Fore.RED + "[!] Nomor tidak valid untuk wilayah Indonesia.")
            return

        # Ekstraksi Data
        provider = carrier.name_for_number(parsed, "en")
        location = geocoder.description_for_number(parsed, "id") # Menggunakan bahasa Indonesia
        tz = timezone.time_zones_for_number(parsed)
        hustle_loc = get_indonesia_location(num_input)

        print(Fore.CYAN + "\n[+] HASIL ANALISIS:")
        print(f"    Nomor E164   : {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"    Operator     : {provider if provider else 'Tidak Terdeteksi'}")
        print(f"    Provinsi/Kota: {location if location else 'Indonesia'}")
        print(f"    Info Prefix  : {hustle_loc}")
        print(f"    Zona Waktu   : {', '.join(tz)}")
        print(f"    Tipe Nomor   : {('Mobile' if phonenumbers.number_type(parsed) == 1 else 'Fixed Line')}")

    except Exception as e:
        print(Fore.RED + f"[!] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    banner()
    target = input(Fore.WHITE + "\n[>] Masukkan No HP (Contoh: 0812xxxx atau +62812xxxx): ")
    analyze_indonesia_number(target)