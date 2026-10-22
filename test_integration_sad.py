"""Tests for invalid prediction requests."""

from io import BytesIO


def test_missing_file(client, prediction_mock):
    """Reject an upload with an empty filename."""
    response = client.post(
        "/prediction",
        data={"file": (BytesIO(b""), "")},
    )

    assert response.status_code == 400
    assert b"Please upload an image file." in response.data
    prediction_mock.assert_not_called()


def test_invalid_image_content(client, prediction_mock):
    """Reject non-image bytes despite a .jpg filename."""
    response = client.post(
        "/prediction",
        data={"file": (BytesIO(b"not an image"), "invalid.jpg")},
    )

    assert response.status_code == 400
    assert b"File cannot be processed." in response.data
    prediction_mock.assert_not_called()
