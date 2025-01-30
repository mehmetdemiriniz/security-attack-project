"""
Güvenlik Uyumluluk Denetleyicisi CLI arayüzü.
Bu modül, güvenlik uyumluluk denetleyicisinin komut satırı arayüzünü sağlar.
"""

import os
import sys
import json
import click
import logging
from datetime import datetime
from typing import Optional, List
from .compliance_checker import GuvenlikDenetleyici, UyumlulukDurumu

# Loglama yapılandırması
def setup_logging(verbose: bool):
    """Loglama seviyesini ayarlar."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_custom_rules(rules_file: str) -> List[dict]:
    """Özel kural dosyasını yükler."""
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
            if not isinstance(rules, dict) or 'rules' not in rules:
                raise ValueError("Geçersiz kural dosyası formatı")
            return rules['rules']
    except Exception as e:
        click.echo(f"Hata: Özel kural dosyası yüklenemedi - {e}", err=True)
        sys.exit(1)

@click.group()
def cli():
    """Güvenlik Uyumluluk Denetleyicisi CLI arayüzü."""
    pass

@cli.command()
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Rapor çıktı dosyası (varsayılan: guvenlik_denetim_raporu_TARIH.json)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['json', 'text']),
    default='json',
    help='Rapor formatı (varsayılan: json)'
)
@click.option(
    '--rules', '-r',
    type=click.Path(exists=True),
    help='Özel kural dosyası yolu'
)
@click.option(
    '--category', '-c',
    multiple=True,
    help='Denetlenecek kural kategorileri (birden fazla belirtilebilir)'
)
@click.option(
    '--level', '-l',
    type=click.Choice(['dusuk', 'orta', 'yuksek', 'kritik']),
    multiple=True,
    help='Denetlenecek kural seviyeleri (birden fazla belirtilebilir)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Detaylı loglama modunu etkinleştirir'
)
def denetle(
    output: Optional[str],
    format: str,
    rules: Optional[str],
    category: tuple,
    level: tuple,
    verbose: bool
):
    """Sistem güvenlik uyumluluğunu denetler."""
    
    # Loglama seviyesini ayarla
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Güvenlik denetleyicisini başlat
        denetleyici = GuvenlikDenetleyici()
        
        # Özel kuralları yükle
        if rules:
            denetleyici.kurallar = load_custom_rules(rules)
        
        # Kategori ve seviye filtrelerini uygula
        if category or level:
            filtered_rules = []
            for kural in denetleyici.kurallar:
                if (not category or kural['category'] in category) and \
                   (not level or kural['level'] in level):
                    filtered_rules.append(kural)
            denetleyici.kurallar = filtered_rules
        
        # Denetimi gerçekleştir
        rapor = denetleyici.denetle()
        
        # Rapor dosya adını belirle
        if not output:
            output = f"guvenlik_denetim_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output += ".json" if format == 'json' else ".txt"
        
        # Raporu kaydet
        if format == 'json':
            denetleyici.kaydet_rapor(rapor, output)
        else:
            # Metin formatında rapor oluştur
            with open(output, 'w', encoding='utf-8') as f:
                f.write(f"Güvenlik Denetim Raporu\n")
                f.write(f"======================\n\n")
                f.write(f"Sistem Adı: {rapor.sistem_adi}\n")
                f.write(f"Sistem Tipi: {rapor.sistem_tipi.value}\n")
                f.write(f"Denetim Tarihi: {rapor.denetim_tarihi}\n\n")
                
                f.write("Denetim Özeti\n")
                f.write("-------------\n")
                f.write(f"Toplam Kural: {rapor.toplam_kural}\n")
                f.write(f"Uyumlu: {rapor.uyumlu_kural}\n")
                f.write(f"Uyumsuz: {rapor.uyumsuz_kural}\n")
                f.write(f"Kontrol Edilemedi: {rapor.kontrol_edilemeyen_kural}\n\n")
                
                f.write("Detaylı Sonuçlar\n")
                f.write("----------------\n")
                for sonuc in rapor.sonuclar:
                    f.write(f"\nKural ID: {sonuc.kural_id}\n")
                    f.write(f"Başlık: {sonuc.baslik}\n")
                    f.write(f"Durum: {sonuc.durum.value}\n")
                    f.write(f"Mevcut Değer: {sonuc.mevcut_deger}\n")
                    f.write(f"Beklenen Değer: {sonuc.beklenen_deger}\n")
                    f.write(f"Düzeltme Önerisi: {sonuc.duzeltme_onerisi}\n")
                    if sonuc.detaylar:
                        f.write(f"Detaylar: {sonuc.detaylar}\n")
        
        # Özet bilgileri göster
        click.echo("\nDenetim Özeti:")
        click.echo(f"Toplam Kural: {rapor.toplam_kural}")
        click.echo(f"Uyumlu: {rapor.uyumlu_kural}")
        click.echo(f"Uyumsuz: {rapor.uyumsuz_kural}")
        click.echo(f"Kontrol Edilemedi: {rapor.kontrol_edilemeyen_kural}")
        click.echo(f"\nDetaylı rapor kaydedildi: {output}")
        
        # Başarısız durumda çıkış kodu döndür
        if rapor.uyumsuz_kural > 0 or rapor.kontrol_edilemeyen_kural > 0:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Program çalışırken hata: {e}")
        sys.exit(1)

@cli.command()
@click.argument('rapor_dosyasi', type=click.Path(exists=True))
def analiz(rapor_dosyasi: str):
    """Denetim raporunu analiz eder ve özet bilgiler sunar."""
    try:
        with open(rapor_dosyasi, 'r', encoding='utf-8') as f:
            rapor = json.load(f)
        
        # Kategori bazlı analiz
        kategoriler = {}
        for sonuc in rapor['sonuclar']:
            kategori = sonuc.get('kategori', 'Diğer')
            if kategori not in kategoriler:
                kategoriler[kategori] = {
                    'toplam': 0,
                    'uyumlu': 0,
                    'uyumsuz': 0,
                    'kontrol_edilemedi': 0
                }
            
            kategoriler[kategori]['toplam'] += 1
            if sonuc['durum'] == UyumlulukDurumu.UYUMLU.value:
                kategoriler[kategori]['uyumlu'] += 1
            elif sonuc['durum'] == UyumlulukDurumu.UYUMSUZ.value:
                kategoriler[kategori]['uyumsuz'] += 1
            else:
                kategoriler[kategori]['kontrol_edilemedi'] += 1
        
        # Analiz sonuçlarını göster
        click.echo("\nKategori Bazlı Analiz:")
        click.echo("=====================")
        
        for kategori, sayilar in kategoriler.items():
            click.echo(f"\n{kategori}:")
            click.echo(f"  Toplam: {sayilar['toplam']}")
            click.echo(f"  Uyumlu: {sayilar['uyumlu']}")
            click.echo(f"  Uyumsuz: {sayilar['uyumsuz']}")
            click.echo(f"  Kontrol Edilemedi: {sayilar['kontrol_edilemedi']}")
            
            # Uyumluluk yüzdesi
            if sayilar['toplam'] > 0:
                uyumluluk = (sayilar['uyumlu'] / sayilar['toplam']) * 100
                click.echo(f"  Uyumluluk Oranı: %{uyumluluk:.1f}")
        
        # Genel uyumluluk durumu
        toplam = rapor['ozet']['toplam_kural']
        uyumlu = rapor['ozet']['uyumlu_kural']
        genel_uyumluluk = (uyumlu / toplam) * 100 if toplam > 0 else 0
        
        click.echo("\nGenel Uyumluluk Durumu:")
        click.echo("=======================")
        click.echo(f"Genel Uyumluluk Oranı: %{genel_uyumluluk:.1f}")
        
        # Öneriler
        click.echo("\nÖneriler:")
        click.echo("========")
        for sonuc in rapor['sonuclar']:
            if sonuc['durum'] == UyumlulukDurumu.UYUMSUZ.value:
                click.echo(f"\n[{sonuc['kural_id']}] {sonuc['baslik']}:")
                click.echo(f"  Düzeltme Önerisi: {sonuc['duzeltme_onerisi']}")
        
    except Exception as e:
        click.echo(f"Hata: Rapor analiz edilirken bir hata oluştu - {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli() 