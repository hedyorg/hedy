import hedy.translation as ht


def test_lang_switch_table(monkeypatch):
    nl_11 = ht.lang_switch_table(11, 'nl')
    assert nl_11[('add', 'to')] == ('voeg', 'toe aan')  # issues/3937

    assert ('echo',) in ht.lang_switch_table(1, 'es')
    assert ('echo',) not in ht.lang_switch_table(2, 'es')

    assert ('if',) not in ht.lang_switch_table(4, 'nl')
    assert ('if',) in ht.lang_switch_table(5, 'nl')

    # Simulate a missing translation instead of relying on a language that
    # happens to be incomplete, since Weblate eventually fills those in.
    zh_hant_keywords = dict(ht.hedy_content.KEYWORDS['zh_Hant'])
    del zh_hant_keywords['for']
    monkeypatch.setitem(ht.hedy_content.KEYWORDS, 'zh_Hant', zh_hant_keywords)
    incomplete_xlation = ht.lang_switch_table(16, 'zh_Hant')
    assert incomplete_xlation[('for',)] == ('for',), "should fall back for incomplete xlations"

    assert ht.lang_switch_table(11, 'en', 'nl') == nl_11
