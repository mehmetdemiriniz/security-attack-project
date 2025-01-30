"""
Güvenlik Metrik Gösterge Paneli veri toplama modülü.
Bu modül, güvenlik metriklerini toplar ve analiz eder.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Loglama yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetrikTipi(Enum):
    """Metrik tipleri."""
    ZAFIYET = "zafiyet"
    UYUMLULUK = "uyumluluk"
    OLAY = "olay"
    PERFORMANS = "performans"

class MetrikSeviyesi(Enum):
    """Metrik seviyeleri."""
    KRITIK = "kritik"
    YUKSEK = "yuksek"
    ORTA = "orta"
    DUSUK = "dusuk"
    BILGI = "bilgi"

@dataclass
class GüvenlikMetriği:
    """Güvenlik metriği veri sınıfı."""
    metrik_id: str
    ad: str
    tip: MetrikTipi
    seviye: MetrikSeviyesi
    deger: float
    birim: str
    tarih: datetime
    kaynak: str
    detaylar: Optional[Dict] = None

class MetrikToplayici:
    """Güvenlik metrikleri toplama sınıfı."""
    
    def __init__(self, veri_dizini: str):
        """
        Metrik toplayıcı başlatıcı.
        
        Args:
            veri_dizini: Metrik verilerinin saklanacağı dizin
        """
        self.veri_dizini = veri_dizini
        os.makedirs(veri_dizini, exist_ok=True)
    
    def zafiyet_metrikleri_topla(self, rapor_dosyalari: List[str]) -> List[GüvenlikMetriği]:
        """
        Zafiyet tarama raporlarından metrikleri toplar.
        
        Args:
            rapor_dosyalari: Zafiyet tarama rapor dosyalarının listesi
            
        Returns:
            Toplanan güvenlik metrikleri listesi
        """
        metrikler = []
        
        for dosya in rapor_dosyalari:
            try:
                with open(dosya, 'r', encoding='utf-8') as f:
                    rapor = json.load(f)
                
                # Zafiyet sayıları
                zafiyetler = {
                    'kritik': 0,
                    'yuksek': 0,
                    'orta': 0,
                    'dusuk': 0,
                    'bilgi': 0
                }
                
                for zafiyet in rapor.get('zafiyetler', []):
                    seviye = zafiyet.get('seviye', '').lower()
                    if seviye in zafiyetler:
                        zafiyetler[seviye] += 1
                
                # Metrikleri oluştur
                for seviye, sayi in zafiyetler.items():
                    metrik = GüvenlikMetriği(
                        metrik_id=f"ZAF-{seviye.upper()}",
                        ad=f"{seviye.capitalize()} Seviye Zafiyet Sayısı",
                        tip=MetrikTipi.ZAFIYET,
                        seviye=MetrikSeviyesi[seviye.upper()],
                        deger=float(sayi),
                        birim="adet",
                        tarih=datetime.now(),
                        kaynak=os.path.basename(dosya),
                        detaylar={
                            'rapor_tarihi': rapor.get('tarih'),
                            'hedef': rapor.get('hedef'),
                            'tarayici': rapor.get('tarayici')
                        }
                    )
                    metrikler.append(metrik)
                
            except Exception as e:
                logger.error(f"Zafiyet raporu işlenirken hata: {e}")
                continue
        
        return metrikler
    
    def uyumluluk_metrikleri_topla(self, rapor_dosyalari: List[str]) -> List[GüvenlikMetriği]:
        """
        Güvenlik uyumluluk raporlarından metrikleri toplar.
        
        Args:
            rapor_dosyalari: Uyumluluk rapor dosyalarının listesi
            
        Returns:
            Toplanan güvenlik metrikleri listesi
        """
        metrikler = []
        
        for dosya in rapor_dosyalari:
            try:
                with open(dosya, 'r', encoding='utf-8') as f:
                    rapor = json.load(f)
                
                # Genel uyumluluk oranı
                toplam = rapor['ozet']['toplam_kural']
                uyumlu = rapor['ozet']['uyumlu_kural']
                oran = (uyumlu / toplam * 100) if toplam > 0 else 0
                
                metrik = GüvenlikMetriği(
                    metrik_id="UYM-GENEL",
                    ad="Genel Uyumluluk Oranı",
                    tip=MetrikTipi.UYUMLULUK,
                    seviye=MetrikSeviyesi.YUKSEK,
                    deger=oran,
                    birim="yüzde",
                    tarih=datetime.now(),
                    kaynak=os.path.basename(dosya),
                    detaylar={
                        'toplam_kural': toplam,
                        'uyumlu_kural': uyumlu,
                        'uyumsuz_kural': rapor['ozet']['uyumsuz_kural'],
                        'kontrol_edilemeyen_kural': rapor['ozet']['kontrol_edilemeyen_kural']
                    }
                )
                metrikler.append(metrik)
                
                # Kategori bazlı uyumluluk oranları
                kategoriler = {}
                for sonuc in rapor['sonuclar']:
                    kategori = sonuc.get('kategori', 'Diğer')
                    if kategori not in kategoriler:
                        kategoriler[kategori] = {'toplam': 0, 'uyumlu': 0}
                    
                    kategoriler[kategori]['toplam'] += 1
                    if sonuc['durum'] == 'uyumlu':
                        kategoriler[kategori]['uyumlu'] += 1
                
                for kategori, sayilar in kategoriler.items():
                    oran = (sayilar['uyumlu'] / sayilar['toplam'] * 100) if sayilar['toplam'] > 0 else 0
                    metrik = GüvenlikMetriği(
                        metrik_id=f"UYM-{kategori.upper()}",
                        ad=f"{kategori} Uyumluluk Oranı",
                        tip=MetrikTipi.UYUMLULUK,
                        seviye=MetrikSeviyesi.ORTA,
                        deger=oran,
                        birim="yüzde",
                        tarih=datetime.now(),
                        kaynak=os.path.basename(dosya),
                        detaylar={
                            'kategori': kategori,
                            'toplam_kural': sayilar['toplam'],
                            'uyumlu_kural': sayilar['uyumlu']
                        }
                    )
                    metrikler.append(metrik)
                
            except Exception as e:
                logger.error(f"Uyumluluk raporu işlenirken hata: {e}")
                continue
        
        return metrikler
    
    def olay_metrikleri_topla(self, baslangic: datetime, bitis: datetime) -> List[GüvenlikMetriği]:
        """
        Güvenlik olaylarından metrikleri toplar.
        
        Args:
            baslangic: Başlangıç tarihi
            bitis: Bitiş tarihi
            
        Returns:
            Toplanan güvenlik metrikleri listesi
        """
        metrikler = []
        
        try:
            # Olay sayıları (örnek veriler)
            olaylar = {
                'kritik': 5,
                'yuksek': 12,
                'orta': 25,
                'dusuk': 40,
                'bilgi': 100
            }
            
            for seviye, sayi in olaylar.items():
                metrik = GüvenlikMetriği(
                    metrik_id=f"OLAY-{seviye.upper()}",
                    ad=f"{seviye.capitalize()} Seviye Olay Sayısı",
                    tip=MetrikTipi.OLAY,
                    seviye=MetrikSeviyesi[seviye.upper()],
                    deger=float(sayi),
                    birim="adet",
                    tarih=datetime.now(),
                    kaynak="SIEM",
                    detaylar={
                        'baslangic': baslangic.isoformat(),
                        'bitis': bitis.isoformat(),
                        'periyot': str(bitis - baslangic)
                    }
                )
                metrikler.append(metrik)
            
        except Exception as e:
            logger.error(f"Olay metrikleri toplanırken hata: {e}")
        
        return metrikler
    
    def performans_metrikleri_topla(self) -> List[GüvenlikMetriği]:
        """
        Güvenlik performans metriklerini toplar.
        
        Returns:
            Toplanan güvenlik metrikleri listesi
        """
        metrikler = []
        
        try:
            # Örnek performans metrikleri
            performans = {
                'ortalama_mudahale_suresi': 45.5,  # dakika
                'ortalama_cozum_suresi': 180.0,    # dakika
                'tekrar_eden_olay_orani': 15.5,    # yüzde
                'yanlis_alarm_orani': 8.2,         # yüzde
                'tespit_orani': 92.5               # yüzde
            }
            
            for ad, deger in performans.items():
                birim = "dakika" if "sure" in ad else "yüzde"
                metrik = GüvenlikMetriği(
                    metrik_id=f"PERF-{ad.upper()}",
                    ad=ad.replace('_', ' ').title(),
                    tip=MetrikTipi.PERFORMANS,
                    seviye=MetrikSeviyesi.ORTA,
                    deger=deger,
                    birim=birim,
                    tarih=datetime.now(),
                    kaynak="Performans İzleme",
                    detaylar={
                        'periyot': 'son 30 gün',
                        'olcum_sayisi': 720  # saatlik ölçüm
                    }
                )
                metrikler.append(metrik)
            
        except Exception as e:
            logger.error(f"Performans metrikleri toplanırken hata: {e}")
        
        return metrikler
    
    def metrikleri_kaydet(self, metrikler: List[GüvenlikMetriği]):
        """
        Metrikleri JSON formatında kaydeder.
        
        Args:
            metrikler: Kaydedilecek metrikler listesi
        """
        try:
            dosya_adi = f"guvenlik_metrikleri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            dosya_yolu = os.path.join(self.veri_dizini, dosya_adi)
            
            metrik_listesi = [
                {
                    'metrik_id': m.metrik_id,
                    'ad': m.ad,
                    'tip': m.tip.value,
                    'seviye': m.seviye.value,
                    'deger': m.deger,
                    'birim': m.birim,
                    'tarih': m.tarih.isoformat(),
                    'kaynak': m.kaynak,
                    'detaylar': m.detaylar
                }
                for m in metrikler
            ]
            
            with open(dosya_yolu, 'w', encoding='utf-8') as f:
                json.dump(metrik_listesi, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Metrikler kaydedildi: {dosya_yolu}")
            
        except Exception as e:
            logger.error(f"Metrikler kaydedilirken hata: {e}")
            raise 