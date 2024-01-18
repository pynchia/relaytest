from datetime import date
from http import HTTPStatus

import pytest

from app.tiers import Tiers
from .utils import load_mock_data


DATE_TODAY = str(date.today())


@pytest.mark.asyncio
async def test_import_dealers_only(client) -> None:
    resp = await client.post(
        f"/earnings/{Tiers.bronze}",
        json=load_mock_data("my_sample_activity_log.json")
    )
    assert resp.status_code == HTTPStatus.CREATED
    earnings = resp.json()
    assert earnings == load_mock_data("my_sample_expected_earnings.json")
