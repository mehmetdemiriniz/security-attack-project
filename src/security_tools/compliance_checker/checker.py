"""
Security Compliance Checker ana modülü
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
import yaml
import re

class ComplianceLevel(Enum):
    """Uyumluluk seviyeleri"""
    CRITICAL = "kritik"
    HIGH = "yüksek"
    MEDIUM = "orta"
    LOW = "düşük"
    INFO = "bilgi"

class ComplianceStatus(Enum):
    """Uyumluluk durumları"""
    PASS = "geçti"
    FAIL = "başarısız"
    WARNING = "uyarı"
    NOT_APPLICABLE = "uygulanamaz"

class ComplianceCategory(Enum):
    """Uyumluluk kategorileri"""
    ACCESS_CONTROL = "erişim_kontrolü"
    AUTHENTICATION = "kimlik_doğrulama"
    AUTHORIZATION = "yetkilendirme"
    DATA_PROTECTION = "veri_koruma"
    LOGGING = "loglama"
    NETWORK_SECURITY = "ağ_güvenliği"
    SYSTEM_HARDENING = "sistem_sertleştirme"
    SECURE_CONFIGURATION = "güvenli_yapılandırma"
    VULNERABILITY_MANAGEMENT = "zafiyet_yönetimi"
    INCIDENT_RESPONSE = "olay_müdahale"

@dataclass
class ComplianceRule:
    """Uyumluluk kuralı veri sınıfı"""
    rule_id: str
    title: str
    description: str
    category: ComplianceCategory
    level: ComplianceLevel
    check_command: str
    remediation: str
    expected_value: str
    references: Optional[List[str]] = None

@dataclass
class ComplianceCheck:
    """Uyumluluk kontrolü veri sınıfı"""
    rule: ComplianceRule
    status: ComplianceStatus
    actual_value: str
    details: str
    evidence: Optional[str] = None

class ComplianceChecker:
    """Uyumluluk denetleyici sınıfı"""
    
    def __init__(self, rules_file: str):
        self.rules = self._load_rules(rules_file)
        
    def _load_rules(self, rules_file: str) -> List[ComplianceRule]:
        """Uyumluluk kurallarını yükle"""
        rules = []
        path = Path(rules_file)
        
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif path.suffix in ['.yml', '.yaml']:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        else:
            raise ValueError("Desteklenmeyen kural dosyası formatı")
        
        for rule_data in data['rules']:
            rule = ComplianceRule(
                rule_id=rule_data['id'],
                title=rule_data['title'],
                description=rule_data['description'],
                category=ComplianceCategory(rule_data['category']),
                level=ComplianceLevel(rule_data['level']),
                check_command=rule_data['check_command'],
                remediation=rule_data['remediation'],
                expected_value=rule_data['expected_value'],
                references=rule_data.get('references')
            )
            rules.append(rule)
            
        return rules
    
    def check_compliance(self, target: str) -> List[ComplianceCheck]:
        """Uyumluluk kontrolü yap"""
        results = []
        
        for rule in self.rules:
            try:
                # Komutu çalıştır ve çıktıyı al
                import subprocess
                command = rule.check_command.format(target=target)
                process = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                actual_value = process.stdout.strip()
                
                # Beklenen değerle karşılaştır
                if self._compare_values(actual_value, rule.expected_value):
                    status = ComplianceStatus.PASS
                    details = "Kural kontrolü başarılı"
                else:
                    status = ComplianceStatus.FAIL
                    details = "Kural kontrolü başarısız"
                
                # Sonucu kaydet
                check = ComplianceCheck(
                    rule=rule,
                    status=status,
                    actual_value=actual_value,
                    details=details,
                    evidence=process.stdout if process.stdout else None
                )
                results.append(check)
                
            except subprocess.TimeoutExpired:
                check = ComplianceCheck(
                    rule=rule,
                    status=ComplianceStatus.WARNING,
                    actual_value="",
                    details="Komut zaman aşımına uğradı",
                    evidence=None
                )
                results.append(check)
                
            except Exception as e:
                check = ComplianceCheck(
                    rule=rule,
                    status=ComplianceStatus.NOT_APPLICABLE,
                    actual_value="",
                    details=f"Kontrol sırasında hata: {str(e)}",
                    evidence=None
                )
                results.append(check)
                
        return results
    
    def _compare_values(self, actual: str, expected: str) -> bool:
        """Gerçek ve beklenen değerleri karşılaştır"""
        # Regex desenini kontrol et
        if expected.startswith('/') and expected.endswith('/'):
            pattern = expected[1:-1]
            return bool(re.match(pattern, actual))
        
        # Tam eşleşme kontrolü
        return actual == expected
    
    def generate_report(self, checks: List[ComplianceCheck]) -> Dict:
        """Uyumluluk raporu oluştur"""
        total_rules = len(checks)
        passed_rules = len([c for c in checks if c.status == ComplianceStatus.PASS])
        failed_rules = len([c for c in checks if c.status == ComplianceStatus.FAIL])
        warning_rules = len([c for c in checks if c.status == ComplianceStatus.WARNING])
        na_rules = len([c for c in checks if c.status == ComplianceStatus.NOT_APPLICABLE])
        
        compliance_score = (passed_rules / (total_rules - na_rules)) * 100 if total_rules > na_rules else 0
        
        return {
            "summary": {
                "total_rules": total_rules,
                "passed_rules": passed_rules,
                "failed_rules": failed_rules,
                "warning_rules": warning_rules,
                "na_rules": na_rules,
                "compliance_score": compliance_score
            },
            "results": [
                {
                    "rule_id": check.rule.rule_id,
                    "title": check.rule.title,
                    "description": check.rule.description,
                    "category": check.rule.category.value,
                    "level": check.rule.level.value,
                    "status": check.status.value,
                    "expected_value": check.rule.expected_value,
                    "actual_value": check.actual_value,
                    "details": check.details,
                    "remediation": check.rule.remediation,
                    "evidence": check.evidence,
                    "references": check.rule.references
                }
                for check in checks
            ],
            "failed_by_category": self._count_failed_by_category(checks),
            "failed_by_level": self._count_failed_by_level(checks)
        }
    
    def _count_failed_by_category(self, checks: List[ComplianceCheck]) -> Dict[str, int]:
        """Kategoriye göre başarısız kural sayısını say"""
        counts = {category.value: 0 for category in ComplianceCategory}
        
        for check in checks:
            if check.status == ComplianceStatus.FAIL:
                counts[check.rule.category.value] += 1
                
        return counts
    
    def _count_failed_by_level(self, checks: List[ComplianceCheck]) -> Dict[str, int]:
        """Seviyeye göre başarısız kural sayısını say"""
        counts = {level.value: 0 for level in ComplianceLevel}
        
        for check in checks:
            if check.status == ComplianceStatus.FAIL:
                counts[check.rule.level.value] += 1
                
        return counts
    
    def save_report(self, report: Dict, output_file: str):
        """Raporu dosyaya kaydet"""
        output_path = Path(output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False) 