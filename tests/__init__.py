from nose import collector
import pytest
from data_collector import FreeDataCollector

collector = FreeDataCollector()

# Test sacral tests collection
def test_collect_sacred_tests():
    texts = collector.collect_sacred_tests()
    assert isinstance(texts, list)
    assert len(texts) > 0
    assert "title" in texts[0]
    assert texts[0]["domain"] == "spiritual"

# Test psychology collection
def test_collect_psychology_resources():
    data = collector.collect_psychology_resources()    
    assert isinstance(data, list)
    assert "category" in data[0]
    assert data[0]["category"] == "psychology"

# Test spirituality collection
def test_collect_spirituality_resources():
        



    