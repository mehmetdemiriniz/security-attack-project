"""
Güvenlik Metrik Gösterge Paneli CLI arayüzü.
Bu modül, metrik toplama ve raporlama için komut satırı arayüzü sağlar.
"""

import os
import json
import click
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from .metrics_collector import MetrikToplayici
from .metrics_analyzer import MetrikAnalizci

# Loglama yapılandırması
def setup_logging(verbose: bool):
    """
    Loglama seviyesini ayarlar.
    
    Args:
        verbose: Detaylı loglama yapılıp yapılmayacağı
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@click.group()
def cli():
    """Güvenlik Metrik Gösterge Paneli komut satırı arayüzü."""
    pass

@cli.command()
@click.option(
    '--zafiyet-raporlari',
    '-z',
    multiple=True,
    help='Zafiyet tarama rapor dosyaları'
)
@click.option(
    '--uyumluluk-raporlari',
    '-u',
    multiple=True,
    help='Güvenlik uyumluluk rapor dosyaları'
)
@click.option(
    '--olay-baslangic',
    '-b',
    type=click.DateTime(),
    default=str(datetime.now() - timedelta(days=30)),
    help='Olay metrikleri başlangıç tarihi (varsayılan: 30 gün önce)'
)
@click.option(
    '--olay-bitis',
    '-s',
    type=click.DateTime(),
    default=str(datetime.now()),
    help='Olay metrikleri bitiş tarihi (varsayılan: şimdi)'
)
@click.option(
    '--veri-dizini',
    '-d',
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default='data/metrics',
    help='Metrik verilerinin saklanacağı dizin'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Detaylı loglama modunu aktifleştirir'
)
def topla(
    zafiyet_raporlari: List[str],
    uyumluluk_raporlari: List[str],
    olay_baslangic: datetime,
    olay_bitis: datetime,
    veri_dizini: str,
    verbose: bool
):
    """
    Güvenlik metriklerini toplar ve kaydeder.
    
    Zafiyet tarama raporları, uyumluluk raporları ve güvenlik olaylarından
    metrikleri toplayarak JSON formatında kaydeder.
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Metrik toplayıcıyı başlat
        toplayici = MetrikToplayici(veri_dizini)
        
        # Metrikleri topla
        metrikler = []
        
        if zafiyet_raporlari:
            logger.info("Zafiyet metrikleri toplanıyor...")
            metrikler.extend(toplayici.zafiyet_metrikleri_topla(zafiyet_raporlari))
        
        if uyumluluk_raporlari:
            logger.info("Uyumluluk metrikleri toplanıyor...")
            metrikler.extend(toplayici.uyumluluk_metrikleri_topla(uyumluluk_raporlari))
        
        logger.info("Olay metrikleri toplanıyor...")
        metrikler.extend(toplayici.olay_metrikleri_topla(olay_baslangic, olay_bitis))
        
        logger.info("Performans metrikleri toplanıyor...")
        metrikler.extend(toplayici.performans_metrikleri_topla())
        
        # Metrikleri kaydet
        toplayici.metrikleri_kaydet(metrikler)
        
        logger.info(f"Toplam {len(metrikler)} metrik toplandı ve kaydedildi.")
        
    except Exception as e:
        logger.error(f"Metrik toplama işlemi başarısız: {e}")
        raise click.ClickException(str(e))

@cli.command()
@click.argument(
    'metrik_dosyasi',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True)
)
@click.option(
    '--cikti-dizini',
    '-c',
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default='reports/metrics',
    help='Rapor çıktılarının kaydedileceği dizin'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Detaylı loglama modunu aktifleştirir'
)
def raporla(
    metrik_dosyasi: str,
    cikti_dizini: str,
    verbose: bool
):
    """
    Metriklerden görsel rapor oluşturur.
    
    Belirtilen metrik dosyasından grafikleri ve özet raporu oluşturarak
    HTML ve JSON formatında kaydeder.
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Metrik analizciyi başlat
        analizci = MetrikAnalizci(os.path.dirname(metrik_dosyasi), cikti_dizini)
        
        # Raporu oluştur
        logger.info("Rapor oluşturuluyor...")
        analizci.rapor_olustur(metrik_dosyasi)
        
        logger.info(f"Rapor başarıyla oluşturuldu: {cikti_dizini}")
        
    except Exception as e:
        logger.error(f"Rapor oluşturma işlemi başarısız: {e}")
        raise click.ClickException(str(e))

@cli.command()
@click.argument(
    'metrik_dosyasi',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True)
)
@click.option(
    '--tip',
    '-t',
    type=click.Choice(['zafiyet', 'uyumluluk', 'olay', 'performans']),
    help='Analiz edilecek metrik tipi'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Detaylı loglama modunu aktifleştirir'
)
def analiz(
    metrik_dosyasi: str,
    tip: Optional[str],
    verbose: bool
):
    """
    Metrik verilerini analiz eder ve özet bilgi gösterir.
    
    Belirtilen metrik dosyasını analiz ederek özet istatistikler sunar.
    İsteğe bağlı olarak belirli bir metrik tipine odaklanabilir.
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Metrik analizciyi başlat
        analizci = MetrikAnalizci(os.path.dirname(metrik_dosyasi), 'reports/metrics')
        
        # Metrikleri yükle ve DataFrame'e dönüştür
        metrikler = analizci.metrikleri_yukle(metrik_dosyasi)
        df = analizci.metrikleri_dataframe_cevir(metrikler)
        
        # Tip filtresi uygula
        if tip:
            df = df[df['tip'] == tip]
            if len(df) == 0:
                raise click.ClickException(f"'{tip}' tipinde metrik bulunamadı")
        
        # Özet rapor oluştur
        ozet = analizci.ozet_rapor_olustur(df)
        
        # Özeti ekrana yazdır
        click.echo("\nGüvenlik Metrikleri Analizi")
        click.echo("=" * 30)
        
        if 'zafiyet_ozeti' in ozet and ozet['zafiyet_ozeti']:
            click.echo("\nZafiyet Özeti:")
            click.echo(f"Toplam Zafiyet: {ozet['zafiyet_ozeti']['toplam_zafiyet']}")
            click.echo("Seviye Dağılımı:")
            for seviye, sayi in ozet['zafiyet_ozeti']['seviye_dagilimi'].items():
                click.echo(f"  {seviye.capitalize()}: {sayi}")
        
        if 'uyumluluk_ozeti' in ozet and ozet['uyumluluk_ozeti']:
            click.echo("\nUyumluluk Özeti:")
            click.echo(f"Genel Uyumluluk: %{ozet['uyumluluk_ozeti']['genel_uyumluluk']:.1f}")
            if 'kategori_uyumluluk' in ozet['uyumluluk_ozeti']:
                click.echo("Kategori Bazlı Uyumluluk:")
                for kategori, oran in ozet['uyumluluk_ozeti']['kategori_uyumluluk'].items():
                    click.echo(f"  {kategori}: %{oran:.1f}")
        
        if 'olay_ozeti' in ozet and ozet['olay_ozeti']:
            click.echo("\nOlay Özeti:")
            click.echo(f"Toplam Olay: {ozet['olay_ozeti']['toplam_olay']}")
            click.echo("Seviye Dağılımı:")
            for seviye, sayi in ozet['olay_ozeti']['seviye_dagilimi'].items():
                click.echo(f"  {seviye.capitalize()}: {sayi}")
        
        if 'performans_ozeti' in ozet and ozet['performans_ozeti']:
            click.echo("\nPerformans Özeti:")
            for metrik, deger in ozet['performans_ozeti'].items():
                click.echo(f"  {metrik}: {deger:.1f}")
        
    except Exception as e:
        logger.error(f"Analiz işlemi başarısız: {e}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli() 