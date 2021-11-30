import unittest
import hedy 
import utils
from website import translating

def check_local_lang_bool(func):
    def inner(self):
        if not hedy.local_keywords_enabled:
            return

        return func(self)

    return inner
  
class TestTranslating(unittest.TestCase):
  def test_change_nested_records(self):
    data = {}
    translating.apply_form_change(data, 'adventures.dice.name', 'x')
    self.assertEqual(data, {
      'adventures': { 'dice': { 'name': 'x' }}
    })

  def test_record_with_int_keys(self):
    data = {}
    translating.apply_form_change(data, 'adventures.3.name', 'x')
    self.assertEqual(data, {
      'adventures': { 3: { 'name': 'x' }}
    })

  def test_array_with_index(self):
    data = {}
    translating.apply_form_change(data, 'adventures.a:0.name', 'x')
    self.assertEqual(data, {
      'adventures': [{ 'name': 'x' }]
    })

  def test_array_with_nonfirst_index(self):
    data = {}
    translating.apply_form_change(data, 'adventures.a:1.name', 'x')
    self.assertEqual(data, {
      'adventures': [{}, { 'name': 'x' }]
    })

  def test_array_with_nonfirst_index_and_two_changes(self):
    data = {}
    translating.apply_form_change(data, 'adventures.a:0.name', 'y')
    translating.apply_form_change(data, 'adventures.a:1.name', 'x')
    self.assertEqual(data, {
      'adventures': [{ 'name': 'y' }, { 'name': 'x' }]
    })