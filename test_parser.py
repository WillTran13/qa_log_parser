import pytest
from log_parser import check_line_for_anomalies

def test_clean_log_line():
    """Test that a normal operational log is NOT flagged."""
    line = "[2026-03-27 10:00:03] [INFO] Screen drivers loaded successfully."
    is_anomaly, reason = check_line_for_anomalies(line)
    assert is_anomaly is False
    assert reason is None

def test_critical_error_flag():
    """Test that ERROR, FATAL, and TIMEOUT are correctly flagged."""
    line = "[2026-03-27 10:15:05] [ERROR] Touch sensor failed to initialize."
    is_anomaly, reason = check_line_for_anomalies(line)
    assert is_anomaly is True
    assert reason == "Critical Error Flag"

def test_acceptable_latency():
    """Test that latency under 50ms is ignored."""
    line = "[2026-03-27 10:00:06] [INFO] Swipe gesture registered. Latency: 12ms."
    is_anomaly, reason = check_line_for_anomalies(line)
    assert is_anomaly is False
    assert reason is None

def test_high_latency_flag():
    """Test that latency over 50ms is flagged accurately."""
    line = "[2026-03-27 10:15:07] [INFO] Swipe gesture registered. Latency: 85ms."
    is_anomaly, reason = check_line_for_anomalies(line)
    assert is_anomaly is True
    assert reason == "High Latency (85ms)"