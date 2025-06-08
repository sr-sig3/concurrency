import pytest
import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "concurrent_user"

@pytest.mark.asyncio
async def test_concurrent_charge_and_use():
    async with httpx.AsyncClient() as client:
        # 먼저 유저 포인트 0으로 초기화
        resp = await client.get(f"{BASE_URL}/points/check/{USER_ID}")
        # get으로 확인된것 만큼 포인트 있는것 사용
        resp = await client.post(f"{BASE_URL}/points/use", json={"user_id": USER_ID, "amount": resp.json()["points"]})

        # 동시에 10번 충전 (각 100포인트)
        charge_tasks = [
            client.post(f"{BASE_URL}/points/charge", json={"user_id": USER_ID, "amount": 100})
            for _ in range(10)
        ]
        charge_responses = await asyncio.gather(*charge_tasks)
        assert all(r.status_code == 200 for r in charge_responses)
        # 충전 후 포인트 확인
        resp = await client.get(f"{BASE_URL}/points/check/{USER_ID}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["points"] == 1000 

        # 동시에 10번 사용 (각 50포인트)
        use_tasks = [
            client.post(f"{BASE_URL}/points/use", json={"user_id": USER_ID, "amount": 50})
            for _ in range(10)
        ]
        use_responses = await asyncio.gather(*use_tasks)
        assert all(r.status_code == 200 for r in use_responses)

        # 최종 포인트 확인 (1000 충전 - 500 사용 = 500)
        resp = await client.get(f"{BASE_URL}/points/check/{USER_ID}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["points"] == 500 