import pytest
import json
import os

# Assuming DetectionNode logic can be tested
def test_mock_logic():
    # Simple placeholder test to demonstrate pytest setup
    assert 1 + 1 == 2

def test_config_loading():
    # Test if we can parse the expected regions format
    dummy_config = [
        {"id": 1, "points": [[10, 10], [50, 10], [50, 50], [10, 50]]}
    ]
    
    region = dummy_config[0]
    pts = region['points']
    x_coords = [p[0] for p in pts]
    y_coords = [p[1] for p in pts]
    x1, y1, x2, y2 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
    
    assert x1 == 10
    assert y1 == 10
    assert x2 == 50
    assert y2 == 50
