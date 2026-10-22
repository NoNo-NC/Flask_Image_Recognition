"""Acceptance tests for image modes and unusual upload conditions."""


def test_edge_case_large_image_upload(
    client, image_factory, prediction_mock
):
    """Accept and resize a high-resolution image."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(size=(2048, 1024)), "large.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()
    assert prediction_mock.call_args.args[0].shape == (1, 224, 224, 3)


def test_edge_case_image_without_metadata(
    client, image_factory, prediction_mock
):
    """Accept an image created without optional metadata."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(), "no_metadata.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()


def test_edge_case_unusual_filename_extension(
    client, image_factory, prediction_mock
):
    """Accept valid PNG content with an unusual filename extension."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(), "image.unknown")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()


def test_edge_case_sequential_image_uploads(
    client, image_factory, prediction_mock
):
    """Process two independent uploads in sequence."""
    for filename in ("first.png", "second.png"):
        response = client.post(
            "/prediction",
            data={"file": (image_factory(), filename)},
        )

        assert response.status_code == 200
        assert b">7</h2>" in response.data

    assert prediction_mock.call_count == 2


def test_edge_case_unexpected_headers(
    client, image_factory, prediction_mock
):
    """Accept a valid image with an additional HTTP header."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(), "image.png")},
        headers={"X-Unexpected-Header": "value"},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()


def test_edge_case_rgba_image(client, image_factory, prediction_mock):
    """Convert a four-channel image into a three-channel model input."""
    response = client.post(
        "/prediction",
        data={"file": (image_factory(mode="RGBA"), "rgba.png")},
    )

    assert response.status_code == 200
    assert b">7</h2>" in response.data
    prediction_mock.assert_called_once()
    assert prediction_mock.call_args.args[0].shape == (1, 224, 224, 3)