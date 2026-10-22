"""Tests connecting Flask routes, preprocessing, and rendered responses."""


def test_home_page(client, prediction_mock):
    """Display the upload page without running inference."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hand Sign Digit" in response.data
    prediction_mock.assert_not_called()


def test_successful_prediction(client, image_factory, prediction_mock):
    """Preprocess an image and render the mocked prediction."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(), "test.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()

    image_batch = prediction_mock.call_args.args[0]
    assert image_batch.shape == (1, 224, 224, 3)
    assert image_batch.min() >= 0
    assert image_batch.max() <= 1
