"""Acceptance tests for valid image uploads."""


def test_acceptance_successful_upload(client, image_factory, prediction_mock):
    """Accept a valid image and display the predicted digit."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(), "image.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()
    assert prediction_mock.call_args.args[0].shape == (1, 224, 224, 3)


def test_acceptance_valid_large_image(client, image_factory, prediction_mock):
    """Accept a high-resolution image."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(size=(1600, 1200)), "large.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()
    assert prediction_mock.call_args.args[0].shape == (1, 224, 224, 3)


def test_acceptance_valid_image_size_upload(
    client, image_factory, prediction_mock
):
    """Accept a small non-square image."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(size=(32, 64)), "small.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()