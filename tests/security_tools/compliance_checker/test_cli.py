"""
Güvenlik Uyumluluk Denetleyicisi CLI test modülü.
"""

import os
import json
import pytest
from click.testing import CliRunner
from datetime import datetime
from unittest.mock import patch, MagicMock
from security_tools.compliance_checker.cli import cli, denetle, analiz
from security_tools.compliance_checker.compliance_checker import (
    GuvenlikDenetleyici,
    SistemTipi,
    UyumlulukDurumu,
    KuralSonucu,
    DenetimRaporu
)

# Test verileri
TEST_RULES = {
    'rules': [
        {
            'id': 'TEST-001',
            'title': 'Test Kuralı 1',
            'description': 'Test açıklaması 1',
            'category': 'test_kategori',
            'level': 'yuksek',
            'check_command': 'echo "test_output"',
            'expected_value': 'test_output',
            'remediation': 'Test düzeltme önerisi 1'
        }
    ]
}

@pytest.fixture
def runner():
    """CLI test runner fixture."""
    return CliRunner()

@pytest.fixture
def mock_denetleyici():
    """Mock denetleyici fixture."""
    with patch('security_tools.compliance_checker.cli.GuvenlikDenetleyici') as mock:
        denetleyici = MagicMock()
        denetleyici.sistem_tipi = SistemTipi.LINUX
        denetleyici.kurallar = TEST_RULES['rules']
        mock.return_value = denetleyici
        yield denetleyici

@pytest.fixture
def test_rapor(tmp_path):
    """Test rapor dosyası fixture."""
    rapor = {
        'sistem_adi': 'test_sistem',
        'sistem_tipi': 'linux',
        'denetim_tarihi': datetime.now().isoformat(),
        'sonuclar': [
            {
                'kural_id': 'TEST-001',
                'baslik': 'Test Kuralı 1',
                'durum': 'uyumlu',
                'mevcut_deger': 'test_output',
                'beklenen_deger': 'test_output',
                'duzeltme_onerisi': 'Test düzeltme önerisi 1',
                'kategori': 'test_kategori'
            },
            {
                'kural_id': 'TEST-002',
                'baslik': 'Test Kuralı 2',
                'durum': 'uyumsuz',
                'mevcut_deger': 'yanlis_deger',
                'beklenen_deger': 'dogru_deger',
                'duzeltme_onerisi': 'Test düzeltme önerisi 2',
                'kategori': 'test_kategori'
            }
        ],
        'ozet': {
            'toplam_kural': 2,
            'uyumlu_kural': 1,
            'uyumsuz_kural': 1,
            'kontrol_edilemeyen_kural': 0
        }
    }
    
    rapor_dosyasi = tmp_path / 'test_rapor.json'
    with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
        json.dump(rapor, f)
    
    return str(rapor_dosyasi)

def test_cli_denetle_varsayilan(runner, mock_denetleyici):
    """CLI denetle komutu varsayılan parametrelerle test."""
    # Mock rapor oluştur
    mock_rapor = DenetimRaporu(
        sistem_adi='test_sistem',
        sistem_tipi=SistemTipi.LINUX,
        denetim_tarihi=datetime.now(),
        sonuclar=[
            KuralSonucu(
                kural_id='TEST-001',
                baslik='Test Kuralı 1',
                durum=UyumlulukDurumu.UYUMLU,
                mevcut_deger='test_output',
                beklenen_deger='test_output',
                duzeltme_onerisi='Test düzeltme önerisi 1'
            )
        ],
        toplam_kural=1,
        uyumlu_kural=1,
        uyumsuz_kural=0,
        kontrol_edilemeyen_kural=0
    )
    mock_denetleyici.denetle.return_value = mock_rapor
    
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert 'Denetim Özeti:' in result.output
    assert 'Toplam Kural: 1' in result.output
    assert 'Uyumlu: 1' in result.output
    assert 'Uyumsuz: 0' in result.output
    assert 'Kontrol Edilemedi: 0' in result.output

def test_cli_denetle_ozel_cikti(runner, mock_denetleyici, tmp_path):
    """CLI denetle komutu özel çıktı dosyasıyla test."""
    # Mock rapor oluştur
    mock_rapor = DenetimRaporu(
        sistem_adi='test_sistem',
        sistem_tipi=SistemTipi.LINUX,
        denetim_tarihi=datetime.now(),
        sonuclar=[
            KuralSonucu(
                kural_id='TEST-001',
                baslik='Test Kuralı 1',
                durum=UyumlulukDurumu.UYUMLU,
                mevcut_deger='test_output',
                beklenen_deger='test_output',
                duzeltme_onerisi='Test düzeltme önerisi 1'
            )
        ],
        toplam_kural=1,
        uyumlu_kural=1,
        uyumsuz_kural=0,
        kontrol_edilemeyen_kural=0
    )
    mock_denetleyici.denetle.return_value = mock_rapor
    
    # Çıktı dosyası yolu
    output_file = tmp_path / 'test_output.json'
    
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle', '--output', str(output_file)])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert output_file.exists()
    assert f'Detaylı rapor kaydedildi: {output_file}' in result.output

def test_cli_denetle_text_format(runner, mock_denetleyici, tmp_path):
    """CLI denetle komutu metin formatında test."""
    # Mock rapor oluştur
    mock_rapor = DenetimRaporu(
        sistem_adi='test_sistem',
        sistem_tipi=SistemTipi.LINUX,
        denetim_tarihi=datetime.now(),
        sonuclar=[
            KuralSonucu(
                kural_id='TEST-001',
                baslik='Test Kuralı 1',
                durum=UyumlulukDurumu.UYUMLU,
                mevcut_deger='test_output',
                beklenen_deger='test_output',
                duzeltme_onerisi='Test düzeltme önerisi 1'
            )
        ],
        toplam_kural=1,
        uyumlu_kural=1,
        uyumsuz_kural=0,
        kontrol_edilemeyen_kural=0
    )
    mock_denetleyici.denetle.return_value = mock_rapor
    
    # Çıktı dosyası yolu
    output_file = tmp_path / 'test_output.txt'
    
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle', '--output', str(output_file), '--format', 'text'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert output_file.exists()
    
    # Metin dosyasının içeriğini kontrol et
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'Güvenlik Denetim Raporu' in content
        assert 'Denetim Özeti' in content
        assert 'Detaylı Sonuçlar' in content

def test_cli_denetle_kategori_filtresi(runner, mock_denetleyici):
    """CLI denetle komutu kategori filtresiyle test."""
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle', '--category', 'test_kategori'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert mock_denetleyici.denetle.called

def test_cli_denetle_seviye_filtresi(runner, mock_denetleyici):
    """CLI denetle komutu seviye filtresiyle test."""
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle', '--level', 'yuksek'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert mock_denetleyici.denetle.called

def test_cli_analiz(runner, test_rapor):
    """CLI analiz komutu testi."""
    # Komutu çalıştır
    result = runner.invoke(cli, ['analiz', test_rapor])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert 'Kategori Bazlı Analiz:' in result.output
    assert 'Genel Uyumluluk Durumu:' in result.output
    assert 'Öneriler:' in result.output
    assert 'test_kategori' in result.output
    assert 'Uyumluluk Oranı: %50.0' in result.output

def test_cli_analiz_hatali_dosya(runner):
    """CLI analiz komutu hatalı dosya testi."""
    # Komutu çalıştır
    result = runner.invoke(cli, ['analiz', 'olmayan_dosya.json'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 1
    assert 'Hata:' in result.output

def test_cli_denetle_verbose(runner, mock_denetleyici):
    """CLI denetle komutu verbose mod testi."""
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle', '--verbose'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 0
    assert mock_denetleyici.denetle.called

def test_cli_denetle_basarisiz(runner, mock_denetleyici):
    """CLI denetle komutu başarısız durum testi."""
    # Mock rapor oluştur
    mock_rapor = DenetimRaporu(
        sistem_adi='test_sistem',
        sistem_tipi=SistemTipi.LINUX,
        denetim_tarihi=datetime.now(),
        sonuclar=[
            KuralSonucu(
                kural_id='TEST-001',
                baslik='Test Kuralı 1',
                durum=UyumlulukDurumu.UYUMSUZ,
                mevcut_deger='yanlis_deger',
                beklenen_deger='dogru_deger',
                duzeltme_onerisi='Test düzeltme önerisi 1'
            )
        ],
        toplam_kural=1,
        uyumlu_kural=0,
        uyumsuz_kural=1,
        kontrol_edilemeyen_kural=0
    )
    mock_denetleyici.denetle.return_value = mock_rapor
    
    # Komutu çalıştır
    result = runner.invoke(cli, ['denetle'])
    
    # Sonuçları kontrol et
    assert result.exit_code == 1
    assert 'Uyumsuz: 1' in result.output 