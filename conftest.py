"""Shared fixtures for Flask route tests."""

from io import BytesIO
from unittest.mock import Mock

import pytest
from PIL import Image

import app as app_module


@pytest.fixture
def prediction_mock(monkeypatch):
    """Replace route-level inference with a deterministic prediction."""
    predictor = Mock(return_value=7)
    monkeypatch.setattr(app_module, "predict_result", predictor)
    return predictor


@pytest.fixture
def client(prediction_mock, monkeypatch):
    """Provide a Flask client with real preprocessing and mocked inference."""
    monkeypatch.setitem(app_module.app.config, "TESTING", True)
    with app_module.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def image_factory():
    """Create a fresh valid PNG stream for each upload."""
    def make_image(size=(224, 224), mode="RGB"):
        stream = BytesIO()
        Image.new(mode, size, color=0).save(stream, format="PNG")
        stream.seek(0)
        return stream

    return make_image
