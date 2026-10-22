"""Acceptance tests for missing uploads."""


def test_acceptance_missing_file(client, prediction_mock):
    """Reject a request without an uploaded file."""
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert b"Please upload an image file." in response.data
    prediction_mock.assert_not_called()