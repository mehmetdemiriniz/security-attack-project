"""
Güvenlik Uyumluluk Denetleyicisi ana modülü.
Bu modül, sistemlerin güvenlik politikalarına uyumluluğunu kontrol eder.
"""

import os
import sys
import yaml
import json
import logging
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

# Loglama yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SistemTipi(Enum):
    """Desteklenen sistem tipleri."""
    LINUX = "linux"
    WINDOWS = "windows"

class UyumlulukDurumu(Enum):
    """Kural uyumluluk durumları."""
    UYUMLU = "uyumlu"
    UYUMSUZ = "uyumsuz"
    KONTROL_EDILEMEDI = "kontrol_edilemedi"

@dataclass
class KuralSonucu:
    """Kural denetim sonucu."""
    kural_id: str
    baslik: str
    durum: UyumlulukDurumu
    mevcut_deger: str
    beklenen_deger: str
    duzeltme_onerisi: str
    detaylar: Optional[str] = None

@dataclass
class DenetimRaporu:
    """Denetim raporu."""
    sistem_adi: str
    sistem_tipi: SistemTipi
    denetim_tarihi: datetime
    sonuclar: List[KuralSonucu]
    toplam_kural: int
    uyumlu_kural: int
    uyumsuz_kural: int
    kontrol_edilemeyen_kural: int

class GuvenlikDenetleyici:
    """Güvenlik uyumluluk denetleyicisi ana sınıfı."""
    
    def __init__(self):
        """Güvenlik denetleyicisi başlatıcı."""
        self.sistem_tipi = self._tespit_sistem_tipi()
        self.kurallar = self._yukle_kurallar()
        
    def _tespit_sistem_tipi(self) -> SistemTipi:
        """Sistem tipini tespit eder."""
        sistem = platform.system().lower()
        if sistem == "linux":
            return SistemTipi.LINUX
        elif sistem == "windows":
            return SistemTipi.WINDOWS
        else:
            raise ValueError(f"Desteklenmeyen sistem tipi: {sistem}")

    def _yukle_kurallar(self) -> List[Dict]:
        """Sistem tipine göre kuralları yükler."""
        kural_dosyasi = (
            "linux_security_rules.yaml" 
            if self.sistem_tipi == SistemTipi.LINUX 
            else "windows_security_rules.yaml"
        )
        
        kural_yolu = os.path.join(
            os.path.dirname(__file__),
            "rules",
            kural_dosyasi
        )
        
        try:
            with open(kural_yolu, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)['rules']
        except Exception as e:
            logger.error(f"Kural dosyası yüklenirken hata: {e}")
            raise

    def _calistir_komut(self, komut: str) -> tuple[int, str, str]:
        """Komutu çalıştırır ve sonucu döndürür."""
        try:
            if self.sistem_tipi == SistemTipi.WINDOWS:
                # Windows'ta PowerShell komutlarını çalıştır
                komut = f"powershell -Command {komut}"
            
            process = subprocess.Popen(
                komut,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )
            stdout, stderr = process.communicate()
            return process.returncode, stdout, stderr
        except Exception as e:
            logger.error(f"Komut çalıştırılırken hata: {e}")
            return -1, "", str(e)

    def _degerlendir_sonuc(self, kural: Dict, cikti: str) -> UyumlulukDurumu:
        """Komut çıktısını değerlendirir ve uyumluluk durumunu döndürür."""
        try:
            beklenen = kural['expected_value']
            if beklenen.startswith('/') and beklenen.endswith('/'):
                # Regex kontrolü
                import re
                pattern = beklenen[1:-1]
                if re.search(pattern, cikti):
                    return UyumlulukDurumu.UYUMLU
            else:
                # Tam eşleşme kontrolü
                if beklenen in cikti:
                    return UyumlulukDurumu.UYUMLU
            return UyumlulukDurumu.UYUMSUZ
        except Exception as e:
            logger.error(f"Sonuç değerlendirilirken hata: {e}")
            return UyumlulukDurumu.KONTROL_EDILEMEDI

    def denetle(self) -> DenetimRaporu:
        """Sistem güvenlik uyumluluğunu denetler."""
        sonuclar = []
        uyumlu = 0
        uyumsuz = 0
        kontrol_edilemedi = 0

        for kural in self.kurallar:
            logger.info(f"Denetleniyor: {kural['id']} - {kural['title']}")
            
            returncode, stdout, stderr = self._calistir_komut(kural['check_command'])
            
            if returncode == 0:
                durum = self._degerlendir_sonuc(kural, stdout)
            else:
                durum = UyumlulukDurumu.KONTROL_EDILEMEDI
                logger.error(f"Komut başarısız: {stderr}")

            sonuc = KuralSonucu(
                kural_id=kural['id'],
                baslik=kural['title'],
                durum=durum,
                mevcut_deger=stdout.strip(),
                beklenen_deger=kural['expected_value'],
                duzeltme_onerisi=kural['remediation'],
                detaylar=stderr if stderr else None
            )
            
            sonuclar.append(sonuc)
            
            if durum == UyumlulukDurumu.UYUMLU:
                uyumlu += 1
            elif durum == UyumlulukDurumu.UYUMSUZ:
                uyumsuz += 1
            else:
                kontrol_edilemedi += 1

        return DenetimRaporu(
            sistem_adi=platform.node(),
            sistem_tipi=self.sistem_tipi,
            denetim_tarihi=datetime.now(),
            sonuclar=sonuclar,
            toplam_kural=len(self.kurallar),
            uyumlu_kural=uyumlu,
            uyumsuz_kural=uyumsuz,
            kontrol_edilemeyen_kural=kontrol_edilemedi
        )

    def kaydet_rapor(self, rapor: DenetimRaporu, dosya_yolu: str):
        """Denetim raporunu JSON formatında kaydeder."""
        try:
            rapor_dict = {
                "sistem_adi": rapor.sistem_adi,
                "sistem_tipi": rapor.sistem_tipi.value,
                "denetim_tarihi": rapor.denetim_tarihi.isoformat(),
                "sonuclar": [
                    {
                        "kural_id": s.kural_id,
                        "baslik": s.baslik,
                        "durum": s.durum.value,
                        "mevcut_deger": s.mevcut_deger,
                        "beklenen_deger": s.beklenen_deger,
                        "duzeltme_onerisi": s.duzeltme_onerisi,
                        "detaylar": s.detaylar
                    }
                    for s in rapor.sonuclar
                ],
                "ozet": {
                    "toplam_kural": rapor.toplam_kural,
                    "uyumlu_kural": rapor.uyumlu_kural,
                    "uyumsuz_kural": rapor.uyumsuz_kural,
                    "kontrol_edilemeyen_kural": rapor.kontrol_edilemeyen_kural
                }
            }
            
            with open(dosya_yolu, 'w', encoding='utf-8') as f:
                json.dump(rapor_dict, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Rapor kaydedildi: {dosya_yolu}")
        except Exception as e:
            logger.error(f"Rapor kaydedilirken hata: {e}")
            raise

def main():
    """Ana fonksiyon."""
    try:
        denetleyici = GuvenlikDenetleyici()
        rapor = denetleyici.denetle()
        
        # Raporu kaydet
        rapor_dosyasi = f"guvenlik_denetim_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        denetleyici.kaydet_rapor(rapor, rapor_dosyasi)
        
        # Özet bilgileri göster
        print("\nDenetim Özeti:")
        print(f"Toplam Kural: {rapor.toplam_kural}")
        print(f"Uyumlu: {rapor.uyumlu_kural}")
        print(f"Uyumsuz: {rapor.uyumsuz_kural}")
        print(f"Kontrol Edilemedi: {rapor.kontrol_edilemeyen_kural}")
        print(f"\nDetaylı rapor kaydedildi: {rapor_dosyasi}")
        
    except Exception as e:
        logger.error(f"Program çalışırken hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 