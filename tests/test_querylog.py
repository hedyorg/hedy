from website import querylog, log_queue
import unittest

class TestQueryLog(unittest.TestCase):
  def setUp(self):
    self.records = []
    querylog.LOG_QUEUE.set_transmitter(self._fake_transmitter)

  def _fake_transmitter(self, ts, records):
    self.records.extend(records)

  def test_regular_xmit(self):
    with querylog.LogRecord(banaan='geel') as record:
      record.set(bloem='rood')

    querylog.LOG_QUEUE.transmit_now()

    self.assertEqual(len(self.records), 1)
    self.assertEqual(self.records[0]['banaan'], 'geel')
    self.assertEqual(self.records[0]['bloem'], 'rood')

  def test_emergency_recovery(self):
    querylog.begin_global_log_record(banaan='geel')
    querylog.log_value(bloem='rood')

    querylog.emergency_shutdown()

    recovered_queue = log_queue.LogQueue('querylog', batch_window_s=300)
    recovered_queue.try_load_emergency_saves()
    recovered_queue.set_transmitter(self._fake_transmitter)

    self.assertEqual(self.records, [])

    recovered_queue.transmit_now()

    self.assertEqual(self.records[0]['banaan'], 'geel')
    self.assertEqual(self.records[0]['bloem'], 'rood')
    self.assertEqual(self.records[0]['terminated'], True)
