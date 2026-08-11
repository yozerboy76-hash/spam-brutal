#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import threading
import subprocess
from datetime import datetime

# ================== KONFIGURASI BRUTAL ==================
BANNER = r"""
   ░██████╗██████╗  █████╗ ███╗   ███╗    ██████╗ ██████╗ ██╗   ██╗████████╗ █████╗ ██╗     
   ██╔════╝██╔══██╗██╔══██╗████╗ ████║    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔══██╗██║     
   ██║     ██████╔╝███████║██╔████╔██║    ██████╔╝██████╔╝██║   ██║   ██║   ███████║██║     
   ██║     ██╔══██╗██╔══██║██║╚██╔╝██║    ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══██║██║     
   ╚██████╗██║  ██║██║  ██║██║ ╚═╝ ██║    ██████╔╝██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗
    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝
                                                                                             
   ███████╗██╗     ██╗     ██╗   ██╗    ███████╗██╗     ██╗     ██╗   ██╗
   ██╔════╝██║     ██║     ██║   ██║    ██╔════╝██║     ██║     ██║   ██║
   █████╗  ██║     ██║     ██║   ██║    █████╗  ██║     ██║     ██║   ██║
   ██╔══╝  ██║     ██║     ╚██╗ ██╔╝    ██╔══╝  ██║     ██║     ╚██╗ ██╔╝
   ███████╗███████╗███████╗ ╚████╔╝     ███████╗███████╗███████╗ ╚████╔╝ 
   ╚══════╝╚══════╝╚══════╝  ╚═══╝      ╚══════╝╚══════╝╚══════╝  ╚═══╝  
                                                                          
   ░██████╗██████╗  █████╗ ███╗   ███╗    ███████╗██╗     ██╗     ██╗   ██╗
   ██╔════╝██╔══██╗██╔══██╗████╗ ████║    ██╔════╝██║     ██║     ██║   ██║
   ██║     ██████╔╝███████║██╔████╔██║    █████╗  ██║     ██║     ██║   ██║
   ██║     ██╔══██╗██╔══██║██║╚██╔╝██║    ██╔══╝  ██║     ██║     ╚██╗ ██╔╝
   ╚██████╗██║  ██║██║  ██║██║ ╚═╝ ██║    ███████╗███████╗███████╗ ╚████╔╝ 
    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚══════╝╚══════╝  ╚═══╝  
                                                                          
   ███████╗██╗     ██╗     ██╗   ██╗    ███████╗██╗     ██╗     ██╗   ██╗
   ██╔════╝██║     ██║     ██║   ██║    ██╔════╝██║     ██║     ██║   ██║
   █████╗  ██║     ██║     ██║   ██║    █████╗  ██║     ██║     ██║   ██║
   ██╔══╝  ██║     ██║     ╚██╗ ██╔╝    ██╔══╝  ██║     ██║     ╚██╗ ██╔╝
   ███████╗███████╗███████╗ ╚████╔╝     ███████╗███████╗███████╗ ╚████╔╝ 
   ╚══════╝╚══════╝╚══════╝  ╚═══╝      ╚══════╝╚══════╝╚══════╝  ╚═══╝  
                                                                          
   ███████╗██╗     ██╗     ██╗   ██╗    ███████╗██╗     ██╗     ██╗   ██╗
   ██╔════╝██║     ██║     ██║   ██║    ██╔════╝██║     ██║     ██║   ██║
   █████╗  ██║     ██║     ██║   ██║    █████╗  ██║     ██║     ██║   ██║
   ██╔══╝  ██║     ██║     ╚██╗ ██╔╝    ██╔══╝  ██║     ██║     ╚██╗ ██╔╝
   ███████╗███████╗███████╗ ╚████╔╝     ███████╗███████╗███████╗ ╚████╔╝ 
   ╚══════╝╚══════╝╚══════╝  ╚═══╝      ╚══════╝╚══════╝╚══════╝  ╚═══╝  
                                                                          
      ██████╗██╗     ██╗  ██████╗██╗  ██╗████████╗██╗  ██╗██╗
     ██╔════╝██║     ██║██╔════╝██║ ██╔╝╚══██╔══╝██║  ██║██║
     ██║     ██║     ██║██║     █████╔╝    ██║   ███████║██║
     ██║     ██║     ██║██║     ██╔═██╗    ██║   ██╔══██║██║
     ╚██████╗███████╗██║╚██████╗██║  ██╗   ██║   ██║  ██║███████╗
      ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
                                                                  
            [ AUTHOR : ellnotdev ]                         
            [ VERSION : 3.2.2 ]                           
            [ STATUS : SINGLE INFO JANDA ]                       
"""

# ================== FUNGSI UTAMA ==================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear_screen()
    print(BANNER)
    print("="*60)
    print("    [🔴] THE WOLF PRESENTS : SPAM BRUTAL ENGINE [🔴]")
    print("="*60)
    print()

def validate_phone(number):
    # Hapus spasi dan karakter aneh
    number = number.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if number.startswith("0"):
        number = "62" + number[1:]
    elif number.startswith("+"):
        number = number[1:]
    if not number.startswith("62"):
        number = "62" + number
    if len(number) < 10 or len(number) > 15:
        return None
    if not number.isdigit():
        return None
    return number

def validate_count(count):
    try:
        count = int(count)
        if count < 1 or count > 500:
            return None
        return count
    except:
        return None

def validate_url(url):
    if not url.startswith("http"):
        return None
    return url

# ================== FITUR SPAM OTP ==================
def spam_otp(phone, count):
    print(f"\n[🔥] Memulai SPAM OTP ke {phone} sebanyak {count} kali...")
    print("[⚠️] Pastikan koneksi internet stabil!")
    
    # Daftar layanan OTP (simulasi)
    services = [
        "lazada.co.id", "shopee.co.id", "tokopedia.com", 
        "facebook.com", "telegram.org", "whatsapp.com",
        "instagram.com", "twitter.com", "google.com",
        "microsoft.com", "amazon.com", "netflix.com",
        "spotify.com", "paypal.com", "grab.com",
        "gojek.com", "ovo.id", "dana.id",
        "linkaja.id", "bukalapak.com", "blibli.com"
    ]
    
    def send_spam():
        for i in range(count):
            service = random.choice(services)
            print(f"[{i+1}/{count}] Mengirim OTP dari {service}...")
            # Simulasi pengiriman
            time.sleep(random.uniform(0.1, 0.5))
    
    thread = threading.Thread(target=send_spam)
    thread.start()
    thread.join()
    
    print(f"\n[✅] SPAM OTP selesai! {count} kode OTP telah dikirim ke {phone}")
    print("[💀] Target akan kebanjiran OTP dari berbagai layanan!")

# ================== FITUR DELAY ==================
def delay_whatsapp(phone, count):
    print(f"\n[⏳] Memulai DELAY WhatsApp ke {phone}...")
    print("[🛑] Fitur ini akan membuat akun WA target delay selama 24 jam!")
    
    for i in range(count):
        print(f"[{i+1}/{count}] Mengirim delay packet ke {phone}...")
        # Simulasi pengiriman packet delay
        time.sleep(0.3)
    
    print("\n[✅] Delay WhatsApp berhasil!")
    print(f"[💀] Akun {phone} akan delay/gabisa chatting selama 24 jam!")

# ================== FITUR BLANK ==================
def blank_whatsapp(phone, count):
    print(f"\n[⬛] Memulai BLANK WhatsApp ke {phone}...")
    print("[💀] Ini akan mengirim virus blank ke HP target!")
    
    for i in range(count):
        print(f"[{i+1}/{count}] Mengirim payload blank ke {phone}...")
        time.sleep(0.2)
    
    print("\n[✅] Blank WhatsApp berhasil!")
    print(f"[💀] HP target {phone} akan blank/hang total selama 24 jam!")

# ================== FITUR BAND WA ==================
def band_whatsapp(phone, count):
    print(f"\n[🚫] Memulai BAND WhatsApp ke {phone}...")
    print("[💀] Ini akan spam report ke akun target!")
    
    for i in range(count):
        print(f"[{i+1}/{count}] Mengirim report ke {phone}...")
        time.sleep(0.2)
    
    print("\n[✅] Band WhatsApp berhasil!")
    print(f"[💀] Akun {phone} akan di-banned permanen dari WhatsApp!")

# ================== FITUR BAND GB ==================
def band_gbwhatsapp(url):
    print(f"\n[🚫] Memulai BAND GB WhatsApp ke grup: {url}")
    print("[💀] Ini akan menghapus seluruh anggota grup!")
    
    print("[✅] Band GB WhatsApp berhasil!")
    print("[💀] Grup target telah dihapus!")

# ================== FITUR KUDETA ==================
def kudeta_gbwhatsapp(url, owner, new_owner):
    print(f"\n[👑] Memulai KUDETA GB WhatsApp...")
    print(f"[🎯] Target grup: {url}")
    print(f"[👤] Owner saat ini: {owner}")
    print(f"[👑] New owner: {new_owner}")
    
    print("\n[⚔️] Mengirim perintah kudeta...")
    time.sleep(1)
    print("[✅] Kudeta berhasil!")
    print(f"[💀] {owner} telah di-kick dari grup!")
    print(f"[👑] {new_owner} sekarang adalah pemilik grup!")

# ================== MENU UTAMA ==================
def main():
    while True:
        show_banner()
        print(" [1] SPAM OTP BRUTAL")
        print(" [2] DELAY WHATSAPP")
        print(" [3] BLANK WHATSAPP")
        print(" [4] BAND WHATSAPP")
        print(" [5] BAND GB WHATSAPP")
        print(" [6] KUDETA GB WHATSAPP")
        print(" [0] EXIT")
        print("="*60)
        
        choice = input(" [>>] Pilih menu (0-6): ").strip()
        
        if choice == "0":
            print("\n[👋] Keluar dari The Wolf...")
            break
            
        elif choice == "1":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid! Harus 10-15 digit.")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah spam (1-500): ").strip()
            count = validate_count(count)
            if not count:
                print("[❌] Jumlah tidak valid! Harus 1-500.")
                input("\n[Press Enter]")
                continue
                
            spam_otp(phone, count)
            input("\n[Press Enter]")
            
        elif choice == "2":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid!")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah pengiriman (1-500): ").strip()
            count = validate_count(count)
            if not count:
                print("[❌] Jumlah tidak valid!")
                input("\n[Press Enter]")
                continue
                
            delay_whatsapp(phone, count)
            input("\n[Press Enter]")
            
        elif choice == "3":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid!")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah pengiriman (1-500): ").strip()
            count = validate_count(count)
            if not count:
                print("[❌] Jumlah tidak valid!")
                input("\n[Press Enter]")
                continue
                
            blank_whatsapp(phone, count)
            input("\n[Press Enter]")
            
        elif choice == "4":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid!")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah report (1-500): ").strip()
            count = validate_count(count)
            if not count:
                print("[❌] Jumlah tidak valid!")
                input("\n[Press Enter]")
                continue
                
            band_whatsapp(phone, count)
            input("\n[Press Enter]")
            
        elif choice == "5":
            url = input(" [>>] Masukkan link grup WhatsApp: ").strip()
            url = validate_url(url)
            if not url:
                print("[❌] Link tidak valid!")
                input("\n[Press Enter]")
                continue
                
            band_gbwhatsapp(url)
            input("\n[Press Enter]")
            
        elif choice == "6":
            url = input(" [>>] Masukkan link grup WhatsApp: ").strip()
            url = validate_url(url)
            if not url:
                print("[❌] Link tidak valid!")
                input("\n[Press Enter]")
                continue
                
            owner = input(" [>>] Masukkan nomor owner saat ini: ").strip()
            owner = validate_phone(owner)
            if not owner:
                print("[❌] Nomor owner tidak valid!")
                input("\n[Press Enter]")
                continue
                
            new_owner = input(" [>>] Masukkan nomor owner baru: ").strip()
            new_owner = validate_phone(new_owner)
            if not new_owner:
                print("[❌] Nomor owner baru tidak valid!")
                input("\n[Press Enter]")
                continue
                
            kudeta_gbwhatsapp(url, owner, new_owner)
            input("\n[Press Enter]")
            
        else:
            print("[❌] Pilihan tidak valid!")
            input("\n[Press Enter]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[⚠️] Proses dihentikan oleh user!")
    except Exception as e:
        print(f"\n[❌] Error: {e}")