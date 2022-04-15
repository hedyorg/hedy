from tests.Highlighter import HighlightTester

class HighlighterTestLeveL1(HighlightTester):

  def test_a(self):
    self.assertHighlighted(
      'print hello world',
      'KKKKT TTTTTTTTTTT',
    level="level1", lang='en')


  def test_b(self):
    self.assertHighlightedMultiLine(
      'print hello world',
      'KKKKT TTTTTTTTTTT',
      'print hello world',
      'KKKKT TTTTTTTTTTT',
    level="level1", lang='en')


  def test_c(self):
    self.assertHighlighted(
      'print hello world',
      'KKKKK TTTTTTTTTTT',
    level="level1", lang='en')


  def test_d(self):
    self.assertHighlightedMultiLine(
      'print hello world',
      'KKKKK TTTTTTTTTTT',
      'print hello world',
      'KKKKK TTTTTTTTTTT',
    level="level1", lang='en')