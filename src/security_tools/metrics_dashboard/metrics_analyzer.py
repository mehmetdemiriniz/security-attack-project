"""
Güvenlik Metrik Gösterge Paneli analiz ve görselleştirme modülü.
Bu modül, güvenlik metriklerini analiz eder ve görselleştirir.
"""

import os
import json
import logging
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from .metrics_collector import GüvenlikMetriği, MetrikTipi, MetrikSeviyesi

# Loglama yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetrikAnalizci:
    """Güvenlik metrikleri analiz sınıfı."""
    
    def __init__(self, veri_dizini: str, cikti_dizini: str):
        """
        Metrik analizci başlatıcı.
        
        Args:
            veri_dizini: Metrik verilerinin bulunduğu dizin
            cikti_dizini: Görsel çıktıların kaydedileceği dizin
        """
        self.veri_dizini = veri_dizini
        self.cikti_dizini = cikti_dizini
        os.makedirs(cikti_dizini, exist_ok=True)
    
    def metrikleri_yukle(self, dosya_yolu: str) -> List[Dict]:
        """
        Metrik verilerini yükler.
        
        Args:
            dosya_yolu: Metrik verilerinin bulunduğu dosya yolu
            
        Returns:
            Yüklenen metrik verileri listesi
        """
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Metrik verileri yüklenirken hata: {e}")
            raise
    
    def metrikleri_dataframe_cevir(self, metrikler: List[Dict]) -> pd.DataFrame:
        """
        Metrik verilerini pandas DataFrame'e dönüştürür.
        
        Args:
            metrikler: Metrik verileri listesi
            
        Returns:
            Pandas DataFrame
        """
        try:
            df = pd.DataFrame(metrikler)
            df['tarih'] = pd.to_datetime(df['tarih'])
            return df
        except Exception as e:
            logger.error(f"Metrikler DataFrame'e dönüştürülürken hata: {e}")
            raise
    
    def zafiyet_trend_grafigi_olustur(self, df: pd.DataFrame) -> go.Figure:
        """
        Zafiyet trendlerini gösteren çizgi grafik oluşturur.
        
        Args:
            df: Metrik verileri DataFrame'i
            
        Returns:
            Plotly grafik nesnesi
        """
        try:
            # Zafiyet metriklerini filtrele
            zafiyet_df = df[df['tip'] == 'zafiyet'].copy()
            
            # Seviyeye göre grupla
            pivot_df = zafiyet_df.pivot(
                index='tarih',
                columns='seviye',
                values='deger'
            ).fillna(0)
            
            # Grafik oluştur
            fig = go.Figure()
            
            renkler = {
                'kritik': 'red',
                'yuksek': 'orange',
                'orta': 'yellow',
                'dusuk': 'blue',
                'bilgi': 'green'
            }
            
            for seviye in pivot_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=pivot_df.index,
                        y=pivot_df[seviye],
                        name=seviye.capitalize(),
                        line=dict(color=renkler.get(seviye, 'gray')),
                        mode='lines+markers'
                    )
                )
            
            fig.update_layout(
                title='Zafiyet Trendi',
                xaxis_title='Tarih',
                yaxis_title='Zafiyet Sayısı',
                hovermode='x unified',
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Zafiyet trend grafiği oluşturulurken hata: {e}")
            raise
    
    def uyumluluk_pasta_grafigi_olustur(self, df: pd.DataFrame) -> go.Figure:
        """
        Uyumluluk durumunu gösteren pasta grafik oluşturur.
        
        Args:
            df: Metrik verileri DataFrame'i
            
        Returns:
            Plotly grafik nesnesi
        """
        try:
            # Uyumluluk metriklerini filtrele
            uyumluluk_df = df[
                (df['tip'] == 'uyumluluk') & 
                (df['metrik_id'] == 'UYM-GENEL')
            ].copy()
            
            if len(uyumluluk_df) == 0:
                raise ValueError("Uyumluluk verisi bulunamadı")
            
            # En son uyumluluk verilerini al
            son_veri = uyumluluk_df.iloc[-1]
            detaylar = son_veri['detaylar']
            
            degerler = [
                detaylar['uyumlu_kural'],
                detaylar['uyumsuz_kural'],
                detaylar['kontrol_edilemeyen_kural']
            ]
            
            etiketler = [
                'Uyumlu',
                'Uyumsuz',
                'Kontrol Edilemedi'
            ]
            
            renkler = ['green', 'red', 'gray']
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=etiketler,
                    values=degerler,
                    marker=dict(colors=renkler),
                    hole=.3
                )
            ])
            
            fig.update_layout(
                title='Güvenlik Uyumluluk Durumu',
                annotations=[
                    dict(
                        text=f'Toplam Kural: {detaylar["toplam_kural"]}',
                        x=0.5, y=0.5,
                        font_size=12,
                        showarrow=False
                    )
                ]
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Uyumluluk pasta grafiği oluşturulurken hata: {e}")
            raise
    
    def olay_bar_grafigi_olustur(self, df: pd.DataFrame) -> go.Figure:
        """
        Güvenlik olaylarını gösteren bar grafik oluşturur.
        
        Args:
            df: Metrik verileri DataFrame'i
            
        Returns:
            Plotly grafik nesnesi
        """
        try:
            # Olay metriklerini filtrele
            olay_df = df[df['tip'] == 'olay'].copy()
            
            # Seviyeye göre grupla
            olay_df = olay_df.sort_values('seviye')
            
            renkler = {
                'kritik': 'red',
                'yuksek': 'orange',
                'orta': 'yellow',
                'dusuk': 'blue',
                'bilgi': 'green'
            }
            
            fig = go.Figure(data=[
                go.Bar(
                    x=olay_df['seviye'],
                    y=olay_df['deger'],
                    marker_color=[renkler.get(s, 'gray') for s in olay_df['seviye']],
                    text=olay_df['deger'],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title='Güvenlik Olayları Dağılımı',
                xaxis_title='Olay Seviyesi',
                yaxis_title='Olay Sayısı',
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Olay bar grafiği oluşturulurken hata: {e}")
            raise
    
    def performans_radar_grafigi_olustur(self, df: pd.DataFrame) -> go.Figure:
        """
        Güvenlik performans metriklerini gösteren radar grafik oluşturur.
        
        Args:
            df: Metrik verileri DataFrame'i
            
        Returns:
            Plotly grafik nesnesi
        """
        try:
            # Performans metriklerini filtrele
            perf_df = df[df['tip'] == 'performans'].copy()
            
            # Yüzde ve süre metriklerini normalize et
            max_sure = perf_df[perf_df['birim'] == 'dakika']['deger'].max()
            
            degerler = []
            for _, row in perf_df.iterrows():
                if row['birim'] == 'dakika':
                    # Süreleri 0-100 arasına normalize et (ters çevir)
                    deger = 100 * (1 - (row['deger'] / max_sure))
                else:
                    deger = row['deger']
                degerler.append(deger)
            
            fig = go.Figure(data=go.Scatterpolar(
                r=degerler,
                theta=perf_df['ad'],
                fill='toself',
                name='Performans'
            ))
            
            fig.update_layout(
                title='Güvenlik Performans Metrikleri',
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Performans radar grafiği oluşturulurken hata: {e}")
            raise
    
    def ozet_rapor_olustur(self, df: pd.DataFrame) -> Dict:
        """
        Metriklerden özet rapor oluşturur.
        
        Args:
            df: Metrik verileri DataFrame'i
            
        Returns:
            Özet rapor sözlüğü
        """
        try:
            ozet = {
                'tarih': datetime.now().isoformat(),
                'zafiyet_ozeti': {},
                'uyumluluk_ozeti': {},
                'olay_ozeti': {},
                'performans_ozeti': {}
            }
            
            # Zafiyet özeti
            zafiyet_df = df[df['tip'] == 'zafiyet']
            if not zafiyet_df.empty:
                toplam_zafiyet = zafiyet_df['deger'].sum()
                seviye_dagilimi = zafiyet_df.groupby('seviye')['deger'].sum().to_dict()
                
                ozet['zafiyet_ozeti'] = {
                    'toplam_zafiyet': toplam_zafiyet,
                    'seviye_dagilimi': seviye_dagilimi
                }
            
            # Uyumluluk özeti
            uyumluluk_df = df[df['tip'] == 'uyumluluk']
            if not uyumluluk_df.empty:
                genel_uyumluluk = uyumluluk_df[
                    uyumluluk_df['metrik_id'] == 'UYM-GENEL'
                ]['deger'].iloc[-1]
                
                kategori_uyumluluk = uyumluluk_df[
                    uyumluluk_df['metrik_id'] != 'UYM-GENEL'
                ].groupby('ad')['deger'].mean().to_dict()
                
                ozet['uyumluluk_ozeti'] = {
                    'genel_uyumluluk': genel_uyumluluk,
                    'kategori_uyumluluk': kategori_uyumluluk
                }
            
            # Olay özeti
            olay_df = df[df['tip'] == 'olay']
            if not olay_df.empty:
                toplam_olay = olay_df['deger'].sum()
                seviye_dagilimi = olay_df.groupby('seviye')['deger'].sum().to_dict()
                
                ozet['olay_ozeti'] = {
                    'toplam_olay': toplam_olay,
                    'seviye_dagilimi': seviye_dagilimi
                }
            
            # Performans özeti
            perf_df = df[df['tip'] == 'performans']
            if not perf_df.empty:
                performans_ozeti = perf_df.set_index('ad')['deger'].to_dict()
                ozet['performans_ozeti'] = performans_ozeti
            
            return ozet
            
        except Exception as e:
            logger.error(f"Özet rapor oluşturulurken hata: {e}")
            raise
    
    def rapor_olustur(self, metrik_dosyasi: str):
        """
        Metriklerden görsel rapor oluşturur.
        
        Args:
            metrik_dosyasi: Metrik verilerinin bulunduğu dosya
        """
        try:
            # Metrikleri yükle
            metrikler = self.metrikleri_yukle(metrik_dosyasi)
            df = self.metrikleri_dataframe_cevir(metrikler)
            
            # Grafikleri oluştur
            zafiyet_grafik = self.zafiyet_trend_grafigi_olustur(df)
            uyumluluk_grafik = self.uyumluluk_pasta_grafigi_olustur(df)
            olay_grafik = self.olay_bar_grafigi_olustur(df)
            performans_grafik = self.performans_radar_grafigi_olustur(df)
            
            # Özet rapor oluştur
            ozet = self.ozet_rapor_olustur(df)
            
            # Grafikleri kaydet
            tarih = datetime.now().strftime('%Y%m%d_%H%M%S')
            zafiyet_grafik.write_html(
                os.path.join(self.cikti_dizini, f'zafiyet_trend_{tarih}.html')
            )
            uyumluluk_grafik.write_html(
                os.path.join(self.cikti_dizini, f'uyumluluk_durum_{tarih}.html')
            )
            olay_grafik.write_html(
                os.path.join(self.cikti_dizini, f'olay_dagilim_{tarih}.html')
            )
            performans_grafik.write_html(
                os.path.join(self.cikti_dizini, f'performans_radar_{tarih}.html')
            )
            
            # Özet raporu kaydet
            ozet_dosyasi = os.path.join(self.cikti_dizini, f'ozet_rapor_{tarih}.json')
            with open(ozet_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(ozet, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Rapor oluşturuldu: {self.cikti_dizini}")
            
        except Exception as e:
            logger.error(f"Rapor oluşturulurken hata: {e}")
            raise 