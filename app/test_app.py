import unittest
from unittest.mock import Mock, MagicMock, patch
from app import app, bp_app, health


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_health(self):
        response = self.client.get("/health")
        assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()

    # class MockRedisDriver:
    #     def save_word_ts(word: str, ts: float) -> None:
    #         pass
    #     def get_word_ts_list(self, word: str) -> [float]:
    #         return []
    #     def health():
    #         return 'OK2'
    #     def foo():
    #         return 1234

    # RedisDriver.save_word_ts = Mock()
    # RedisDriver.get_word_ts_list = Mock()
    # mockRedisDriver = Mock()
    # RedisDriver.save_word_ts = Mock()
    # RedisDriver = Mock()
    # RedisDriver.save_word_ts = MockRedisDriver.save_word_ts
    # RedisDriver.get_word_ts_list = MockRedisDriver.get_word_ts_list
    # RedisDriver.foo = MockRedisDriver.foo

    # RedisDriver.save_word_ts = self.origin_save_word_ts
    # RedisDriver.get_word_ts_list = self.origin_get_word_ts_list

    # def test_events(self):
    #     response = self.client.get("/events")
    #     self.assertEqual('1234', RedisDriver.save_word_ts('word', 1234.44))

    # def test_stats(self):
    #     response = self.client.get("/stats")
    #     print(response.get_json())
    #     print(response.get_data())
    #     print(response)
    #     self.assertEqual([], response.get_json())