from reports import generate_report
import pytest

def test_generate_report_success():
    data = [{"idade": 25}, {"idade": 40}]
    result = generate_report(data)
    assert result["valido"] is True
    assert result["total"] == 2

def test_generate_report_empty():
    with pytest.raises(ValueError):
        generate_report([])
