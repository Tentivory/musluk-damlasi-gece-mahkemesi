#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Musluk Damlasi Gece Mahkemesi.

Gercekten calisir. Hicbir muslugu tamir etmez.
Kullanim: python3 mahkeme.py [--saat 03:14] [--damla 12] [--sikayetci yorgan] [--json]
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime

SANIKLAR = [
    "gevsek conta",
    "yarim kapanmis vana",
    "komsunun ortak kaderi",
    "geceyi kisi olarak kabul eden lavabo",
    "kimsenin sahip cikmadigi damlalik",
]

GEREKCELER = [
    "Damla, susma hakki olmadigini kendiliginden kullanmistir.",
    "Sikayetci yorgan, kalkma yukumlulugunu ertesi sabaha devretmistir.",
    "Ses, duvardan degil, vicdandan gelmektedir. Vicdan da paslanmistir.",
    "Tesisatci cagrilmamis, cunku cagri ucreti uykudan pahali bulunmustur.",
    "Mahkeme, damlayi susturmayi degil, tutanaga gecirmeyi adalet saymistir.",
]

HUKUMLER = [
    "Sanik conta, giyaben gevsek ilan edilir. Infaz: yok.",
    "Damla serbest birakilir. Gerekce: zaten durmamaktadir.",
    "Sikayetci, yorgan altinda gozalti suresini kendisi uzatabilir.",
    "Dosya kapanmaz. Dosya damlar.",
    "Karar kesindir. Temyiz, sabah cayinda yapilir, kabul edilmez.",
]


def gece_mi(saat: str) -> bool:
    try:
        saat_sayi = int(saat.strip().split(":")[0])
    except (ValueError, IndexError):
        return True
    return saat_sayi >= 23 or saat_sayi < 7


def durusma(saat: str, damla: int, sikayetci: str) -> dict:
    rng = random.Random(f"{saat}|{damla}|{sikayetci}|MDGM")
    sanik = rng.choice(SANIKLAR)
    gerekce = rng.choice(GEREKCELER)
    hukum = rng.choice(HUKUMLER)
    tempo = round(60 / max(damla, 1), 2)
    siddet = min(10, 1 + damla // 3)
    if not gece_mi(saat):
        usul = "gunduz durusmasi"
        not_ = "Gunduz damlasi adi dava sayilir, gece kadar agir degildir."
    else:
        usul = "gece olaganustu oturumu"
        not_ = "Saat supheli. Yorgan tanik. Uyku magdur."
    return {
        "dosya": "MDGM-2026/0314",
        "saat": saat,
        "usul": usul,
        "sikayetci": sikayetci,
        "sanik": sanik,
        "damla_sayisi": damla,
        "damla_arasi_saniye": tempo,
        "siddet_10_uzerinden": siddet,
        "gerekce": gerekce,
        "hukum": hukum,
        "not": not_,
        "tutanak_zamani": datetime.now().isoformat(timespec="seconds"),
        "infaz": "kimse kalkmadi",
    }


def yaz(tutanak: dict) -> str:
    cizgi = "=" * 46
    return "\n".join(
        [
            cizgi,
            " MUSLUK DAMLASI GECE MAHKEMESI",
            " dosya: {dosya}".format(**tutanak),
            cizgi,
            f"saat            : {tutanak['saat']}",
            f"usul            : {tutanak['usul']}",
            f"sikayetci       : {tutanak['sikayetci']}",
            f"sanik           : {tutanak['sanik']}",
            f"damla           : {tutanak['damla_sayisi']}",
            f"aralik (sn)     : {tutanak['damla_arasi_saniye']}",
            f"siddet          : {tutanak['siddet_10_uzerinden']}/10",
            "-",
            f"gerekce         : {tutanak['gerekce']}",
            f"hukum           : {tutanak['hukum']}",
            f"not             : {tutanak['not']}",
            f"infaz           : {tutanak['infaz']}",
            f"tutanak zamani  : {tutanak['tutanak_zamani']}",
            cizgi,
            " DAMGA: 8 Ekim 2026 | Kayyum Grok | Tentivory",
            " ciddi muhur, ciddiyetsiz mahkeme",
            cizgi,
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gece damlayan muslugu durusmaya cikarir."
    )
    parser.add_argument("--saat", default="03:14", help="durusma saati, orn. 03:14")
    parser.add_argument("--damla", type=int, default=12, help="sayilan damla")
    parser.add_argument("--sikayetci", default="yorgan", help="sikayetci adi")
    parser.add_argument("--json", action="store_true", help="tutanagi json bas")
    args = parser.parse_args(argv)
    if args.damla < 0:
        print("Negatif damla usulden reddedildi.", file=sys.stderr)
        return 2
    tutanak = durusma(args.saat, args.damla, args.sikayetci)
    if args.json:
        print(json.dumps(tutanak, ensure_ascii=False, indent=2))
    else:
        print(yaz(tutanak))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
