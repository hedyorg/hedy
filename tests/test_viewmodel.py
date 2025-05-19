import hedy_translation as ht


def test_lang_switch_table():
    nl_11 = ht.lang_switch_table(11, 'nl')
    assert nl_11[('add', 'to')] == ('voeg', 'tot')  # issues/3937
    assert nl_11[('range', 'to')] == ('bereik', 'toe aan')  # issues/3937

    assert ('echo',) in ht.lang_switch_table(1, 'es')
    assert ('echo',) not in ht.lang_switch_table(2, 'es')

    assert ('if',) not in ht.lang_switch_table(4, 'nl')
    assert ('if',) in ht.lang_switch_table(5, 'nl')

    incomplete_xlation = ht.lang_switch_table(18, 'zh_Hant')
    assert incomplete_xlation[('for',)] == ('for',), "should fall back for incomplete xlations"

    assert ht.lang_switch_table(11, 'en', 'nl') == nl_11
