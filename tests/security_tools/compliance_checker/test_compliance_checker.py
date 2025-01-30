"""
Güvenlik Uyumluluk Denetleyicisi test modülü.
"""

import os
import json
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from security_tools.compliance_checker.compliance_checker import (
    GuvenlikDenetleyici,
    SistemTipi,
    UyumlulukDurumu,
    KuralSonucu,
    DenetimRaporu
)

# Test verileri
TEST_LINUX_RULES = {
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
        },
        {
            'id': 'TEST-002',
            'title': 'Test Kuralı 2',
            'description': 'Test açıklaması 2',
            'category': 'test_kategori',
            'level': 'orta',
            'check_command': 'invalid_command',
            'expected_value': 'beklenen_deger',
            'remediation': 'Test düzeltme önerisi 2'
        }
    ]
}

TEST_WINDOWS_RULES = {
    'rules': [
        {
            'id': 'WIN-TEST-001',
            'title': 'Windows Test Kuralı 1',
            'description': 'Windows test açıklaması 1',
            'category': 'test_kategori',
            'level': 'yuksek',
            'check_command': 'Get-Service | Select-Object Name',
            'expected_value': 'Name',
            'remediation': 'Windows test düzeltme önerisi 1'
        }
    ]
}

@pytest.fixture
def linux_denetleyici():
    """Linux denetleyici fixture."""
    with patch('platform.system', return_value='Linux'):
        with patch('security_tools.compliance_checker.compliance_checker.yaml.safe_load', return_value=TEST_LINUX_RULES):
            return GuvenlikDenetleyici()

@pytest.fixture
def windows_denetleyici():
    """Windows denetleyici fixture."""
    with patch('platform.system', return_value='Windows'):
        with patch('security_tools.compliance_checker.compliance_checker.yaml.safe_load', return_value=TEST_WINDOWS_RULES):
            return GuvenlikDenetleyici()

def test_sistem_tipi_tespiti():
    """Sistem tipi tespiti testi."""
    with patch('platform.system', return_value='Linux'):
        denetleyici = GuvenlikDenetleyici()
        assert denetleyici.sistem_tipi == SistemTipi.LINUX
    
    with patch('platform.system', return_value='Windows'):
        denetleyici = GuvenlikDenetleyici()
        assert denetleyici.sistem_tipi == SistemTipi.WINDOWS
    
    with patch('platform.system', return_value='Unknown'):
        with pytest.raises(ValueError):
            GuvenlikDenetleyici()

def test_kural_yukleme(linux_denetleyici):
    """Kural yükleme testi."""
    assert len(linux_denetleyici.kurallar) == 2
    assert linux_denetleyici.kurallar[0]['id'] == 'TEST-001'
    assert linux_denetleyici.kurallar[1]['id'] == 'TEST-002'

def test_komut_calistirma(linux_denetleyici):
    """Komut çalıştırma testi."""
    # Başarılı komut testi
    returncode, stdout, stderr = linux_denetleyici._calistir_komut('echo "test"')
    assert returncode == 0
    assert stdout.strip() == 'test'
    assert stderr == ''
    
    # Başarısız komut testi
    returncode, stdout, stderr = linux_denetleyici._calistir_komut('invalid_command')
    assert returncode != 0
    assert stdout == ''
    assert stderr != ''

def test_sonuc_degerlendirme(linux_denetleyici):
    """Sonuç değerlendirme testi."""
    # Tam eşleşme testi
    kural = {
        'expected_value': 'test_value'
    }
    assert linux_denetleyici._degerlendir_sonuc(kural, 'test_value') == UyumlulukDurumu.UYUMLU
    assert linux_denetleyici._degerlendir_sonuc(kural, 'wrong_value') == UyumlulukDurumu.UYUMSUZ
    
    # Regex eşleşme testi
    kural = {
        'expected_value': '/^test_.*$/'
    }
    assert linux_denetleyici._degerlendir_sonuc(kural, 'test_123') == UyumlulukDurumu.UYUMLU
    assert linux_denetleyici._degerlendir_sonuc(kural, 'wrong_value') == UyumlulukDurumu.UYUMSUZ

def test_denetim(linux_denetleyici):
    """Denetim testi."""
    # Başarılı denetim testi
    with patch.object(linux_denetleyici, '_calistir_komut') as mock_calistir:
        mock_calistir.return_value = (0, 'test_output', '')
        rapor = linux_denetleyici.denetle()
        
        assert isinstance(rapor, DenetimRaporu)
        assert len(rapor.sonuclar) == 2
        assert rapor.uyumlu_kural == 1
        assert rapor.uyumsuz_kural == 1
        assert rapor.kontrol_edilemeyen_kural == 0

def test_rapor_kaydetme(linux_denetleyici, tmp_path):
    """Rapor kaydetme testi."""
    # Test raporu oluştur
    rapor = DenetimRaporu(
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
    
    # Raporu kaydet
    rapor_dosyasi = tmp_path / 'test_rapor.json'
    linux_denetleyici.kaydet_rapor(rapor, str(rapor_dosyasi))
    
    # Kaydedilen raporu kontrol et
    assert rapor_dosyasi.exists()
    with open(rapor_dosyasi, 'r', encoding='utf-8') as f:
        kayitli_rapor = json.load(f)
    
    assert kayitli_rapor['sistem_adi'] == 'test_sistem'
    assert kayitli_rapor['sistem_tipi'] == 'linux'
    assert len(kayitli_rapor['sonuclar']) == 1
    assert kayitli_rapor['sonuclar'][0]['kural_id'] == 'TEST-001'
    assert kayitli_rapor['ozet']['toplam_kural'] == 1
    assert kayitli_rapor['ozet']['uyumlu_kural'] == 1

def test_windows_komut_calistirma(windows_denetleyici):
    """Windows komut çalıştırma testi."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('test_output', '')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        returncode, stdout, stderr = windows_denetleyici._calistir_komut('Get-Service')
        
        assert returncode == 0
        assert stdout == 'test_output'
        assert stderr == ''
        mock_popen.assert_called_with(
            'powershell -Command Get-Service',
            stdout=-1,
            stderr=-1,
            shell=True,
            text=True
        )

def test_farkli_seviye_kategoriler(linux_denetleyici):
    """Farklı seviye ve kategorilerdeki kuralların testi."""
    # Yüksek seviyeli kuralları filtrele
    yuksek_kurallar = [k for k in linux_denetleyici.kurallar if k['level'] == 'yuksek']
    assert len(yuksek_kurallar) == 1
    assert yuksek_kurallar[0]['id'] == 'TEST-001'
    
    # Orta seviyeli kuralları filtrele
    orta_kurallar = [k for k in linux_denetleyici.kurallar if k['level'] == 'orta']
    assert len(orta_kurallar) == 1
    assert orta_kurallar[0]['id'] == 'TEST-002'
    
    # Test kategorisindeki kuralları filtrele
    test_kurallar = [k for k in linux_denetleyici.kurallar if k['category'] == 'test_kategori']
    assert len(test_kurallar) == 2 