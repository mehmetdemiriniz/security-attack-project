"""
Güvenlik Metrik Gösterge Paneli CLI test modülü.
Bu modül, CLI komutlarını test eder.
"""

import os
import json
import pytest
from click.testing import CliRunner
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from security_tools.metrics_dashboard.cli import cli, topla, raporla, analiz

# Test verileri
TEST_ZAFIYET_RAPORU = {
    'zafiyetler': [
        {'seviye': 'kritik', 'detay': 'Test zafiyet 1'},
        {'seviye': 'yuksek', 'detay': 'Test zafiyet 2'},
        {'seviye': 'orta', 'detay': 'Test zafiyet 3'}
    ],
    'tarih': '2024-03-15T10:00:00',
    'hedef': 'test.example.com',
    'tarayici': 'TestScanner'
}

TEST_UYUMLULUK_RAPORU = {
    'ozet': {
        'toplam_kural': 100,
        'uyumlu_kural': 75,
        'uyumsuz_kural': 20,
        'kontrol_edilemeyen_kural': 5
    },
    'sonuclar': [
        {'kategori': 'Parola Politikası', 'durum': 'uyumlu'},
        {'kategori': 'Ağ Güvenliği', 'durum': 'uyumsuz'},
        {'kategori': 'Sistem Güvenliği', 'durum': 'uyumlu'}
    ]
}

TEST_METRIKLER = [
    {
        'metrik_id': 'ZAF-KRITIK',
        'ad': 'Kritik Seviye Zafiyet Sayısı',
        'tip': 'zafiyet',
        'seviye': 'kritik',
        'deger': 5.0,
        'birim': 'adet',
        'tarih': '2024-03-15T10:00:00',
        'kaynak': 'test_rapor.json',
        'detaylar': {'rapor_tarihi': '2024-03-15T10:00:00'}
    },
    {
        'metrik_id': 'UYM-GENEL',
        'ad': 'Genel Uyumluluk Oranı',
        'tip': 'uyumluluk',
        'seviye': 'yuksek',
        'deger': 75.0,
        'birim': 'yüzde',
        'tarih': '2024-03-15T10:00:00',
        'kaynak': 'test_rapor.json',
        'detaylar': {'toplam_kural': 100, 'uyumlu_kural': 75}
    }
]

@pytest.fixture
def runner():
    """CLI test runner fixture."""
    return CliRunner()

@pytest.fixture
def test_files(tmp_path):
    """Test dosyaları fixture."""
    # Zafiyet raporu
    zafiyet_dosya = tmp_path / "zafiyet_rapor.json"
    zafiyet_dosya.write_text(json.dumps(TEST_ZAFIYET_RAPORU))
    
    # Uyumluluk raporu
    uyumluluk_dosya = tmp_path / "uyumluluk_rapor.json"
    uyumluluk_dosya.write_text(json.dumps(TEST_UYUMLULUK_RAPORU))
    
    # Metrik dosyası
    metrik_dosya = tmp_path / "metrikler.json"
    metrik_dosya.write_text(json.dumps(TEST_METRIKLER))
    
    return {
        'zafiyet': str(zafiyet_dosya),
        'uyumluluk': str(uyumluluk_dosya),
        'metrik': str(metrik_dosya)
    }

def test_cli_help(runner):
    """CLI yardım komutunu test eder."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Güvenlik Metrik Gösterge Paneli' in result.output

def test_topla_help(runner):
    """Topla komutu yardımını test eder."""
    result = runner.invoke(cli, ['topla', '--help'])
    assert result.exit_code == 0
    assert 'Güvenlik metriklerini toplar' in result.output

def test_raporla_help(runner):
    """Raporla komutu yardımını test eder."""
    result = runner.invoke(cli, ['raporla', '--help'])
    assert result.exit_code == 0
    assert 'Metriklerden görsel rapor oluşturur' in result.output

def test_analiz_help(runner):
    """Analiz komutu yardımını test eder."""
    result = runner.invoke(cli, ['analiz', '--help'])
    assert result.exit_code == 0
    assert 'Metrik verilerini analiz eder' in result.output

@patch('security_tools.metrics_dashboard.cli.MetrikToplayici')
def test_topla_zafiyet_raporu(mock_toplayici, runner, test_files, tmp_path):
    """Zafiyet raporu toplama işlemini test eder."""
    # Mock ayarları
    mock_instance = mock_toplayici.return_value
    mock_instance.zafiyet_metrikleri_topla.return_value = [TEST_METRIKLER[0]]
    mock_instance.performans_metrikleri_topla.return_value = []
    
    # Komutu çalıştır
    veri_dizini = str(tmp_path / "data")
    result = runner.invoke(cli, [
        'topla',
        '-z', test_files['zafiyet'],
        '-d', veri_dizini,
        '-v'
    ])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert "Zafiyet metrikleri toplanıyor" in result.output
    mock_instance.zafiyet_metrikleri_topla.assert_called_once()
    mock_instance.metrikleri_kaydet.assert_called_once()

@patch('security_tools.metrics_dashboard.cli.MetrikToplayici')
def test_topla_uyumluluk_raporu(mock_toplayici, runner, test_files, tmp_path):
    """Uyumluluk raporu toplama işlemini test eder."""
    # Mock ayarları
    mock_instance = mock_toplayici.return_value
    mock_instance.uyumluluk_metrikleri_topla.return_value = [TEST_METRIKLER[1]]
    mock_instance.performans_metrikleri_topla.return_value = []
    
    # Komutu çalıştır
    veri_dizini = str(tmp_path / "data")
    result = runner.invoke(cli, [
        'topla',
        '-u', test_files['uyumluluk'],
        '-d', veri_dizini,
        '-v'
    ])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert "Uyumluluk metrikleri toplanıyor" in result.output
    mock_instance.uyumluluk_metrikleri_topla.assert_called_once()
    mock_instance.metrikleri_kaydet.assert_called_once()

@patch('security_tools.metrics_dashboard.cli.MetrikAnalizci')
def test_raporla(mock_analizci, runner, test_files, tmp_path):
    """Rapor oluşturma işlemini test eder."""
    # Mock ayarları
    mock_instance = mock_analizci.return_value
    
    # Komutu çalıştır
    cikti_dizini = str(tmp_path / "reports")
    result = runner.invoke(cli, [
        'raporla',
        test_files['metrik'],
        '-c', cikti_dizini,
        '-v'
    ])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert "Rapor oluşturuluyor" in result.output
    mock_instance.rapor_olustur.assert_called_once_with(test_files['metrik'])

@patch('security_tools.metrics_dashboard.cli.MetrikAnalizci')
def test_analiz(mock_analizci, runner, test_files):
    """Analiz işlemini test eder."""
    # Mock ayarları
    mock_instance = mock_analizci.return_value
    mock_instance.metrikleri_yukle.return_value = TEST_METRIKLER
    mock_instance.ozet_rapor_olustur.return_value = {
        'zafiyet_ozeti': {
            'toplam_zafiyet': 5,
            'seviye_dagilimi': {'kritik': 5}
        }
    }
    
    # Komutu çalıştır
    result = runner.invoke(cli, [
        'analiz',
        test_files['metrik'],
        '-t', 'zafiyet',
        '-v'
    ])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert "Güvenlik Metrikleri Analizi" in result.output
    assert "Zafiyet Özeti" in result.output
    mock_instance.metrikleri_yukle.assert_called_once()
    mock_instance.ozet_rapor_olustur.assert_called_once()

@patch('security_tools.metrics_dashboard.cli.MetrikAnalizci')
def test_analiz_tip_bulunamadi(mock_analizci, runner, test_files):
    """Olmayan metrik tipi için analiz işlemini test eder."""
    # Mock ayarları
    mock_instance = mock_analizci.return_value
    mock_instance.metrikleri_yukle.return_value = TEST_METRIKLER
    
    # Komutu çalıştır
    result = runner.invoke(cli, [
        'analiz',
        test_files['metrik'],
        '-t', 'olmayan_tip',
        '-v'
    ])
    
    # Sonuçları kontrol et
    assert result.exit_code == 1
    assert "tipinde metrik bulunamadı" in result.output

def test_gecersiz_dosya(runner):
    """Geçersiz dosya durumunu test eder."""
    result = runner.invoke(cli, [
        'raporla',
        'olmayan_dosya.json',
        '-v'
    ])
    
    assert result.exit_code == 2
    assert "does not exist" in result.output 