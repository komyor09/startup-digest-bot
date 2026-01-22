from app.parsers.vcru import parse_vcru
from app.parsers.rusbase import parse_rusbase

try:
    vcru = parse_vcru()
except Exception as e:
    print("VC.ru parser error:", e)
    vcru = []

try:
    rusbase = parse_rusbase()
except Exception as e:
    print("RB.ru parser error:", e)
    rusbase = []

if not vcru:
    print("VC.ru RSS is empty or unavailable")

if not rusbase:
    print("RB.ru RSS is empty or unavailable")

if vcru:
    print("VC.ru sample:", vcru[0])

if rusbase:
    print("RB.ru sample:", rusbase[0])
