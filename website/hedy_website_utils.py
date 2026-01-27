from flask import g

import hedy
from website_content import KEYWORDS_ADVENTURES, adventures_order_per_level
from website.auth import current_user
from website.flask_hedy import g_db


def load_all_adventures_for_index(customizations, user_programs, all_languages_adventures):
    """
    Loads all the default adventures in a dictionary that will be used to populate
    the index, therefore we only need the titles and short names of the adventures.
    """

    keyword_lang = g.keyword_lang
    adventures = all_languages_adventures[g.lang].get_adventures(keyword_lang)
    all_adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
    for short_name, adventure in adventures.items():
        for level in adventure['levels']:
            all_adventures[int(level)].append({
                'short_name': short_name,
                'name': adventure['name'],
                'is_teacher_adventure': False,
                'is_command_adventure': short_name in KEYWORDS_ADVENTURES
            })
    for level, adventures in all_adventures.items():
        adventures_order = adventures_order_per_level().get(level, [])
        index_map = {v: i for i, v in enumerate(adventures_order)}
        adventures.sort(key=lambda pair: index_map.get(
            pair['short_name'],
            len(adventures_order)))

    sorted_adventures = customizations.get('sorted_adventures')
    if not sorted_adventures:
        return all_adventures
    # We make sure to only get valid levels
    sorted_adventures = {k: v for k, v in sorted_adventures.items() if int(k) <= hedy.HEDY_MAX_LEVEL}

    builtin_map = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
    adventure_ids = []
    for level, order_for_level in sorted_adventures.items():
        if int(level) > hedy.HEDY_MAX_LEVEL:
            continue
        for a in order_for_level:
            if a['from_teacher']:
                adventure_ids.append(a['name'])
        builtin_map[int(level)] = {a['short_name']: a for a in all_adventures[int(level)]}

    teacher_adventure_map = g_db().batch_get_adventures(adventure_ids)
    all_adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
    for level, order_for_level in sorted_adventures.items():
        for adventure in order_for_level:
            if adventure['from_teacher'] and (db_row := teacher_adventure_map.get(adventure['name'])):
                all_adventures[int(level)].append({
                    'short_name': db_row['id'],
                    'name': db_row['name'],
                    'is_teacher_adventure': True,
                    'is_command_adventure': False
                })
            if not adventure['from_teacher'] and (adv := builtin_map[int(level)].get(adventure['name'])):
                all_adventures[int(level)].append(adv)

    for level, adventures in all_adventures.items():
        for adventure in adventures:
            if adventure['short_name'] not in user_programs.get(level, {}):
                continue
            name = adventure['short_name']
            student_adventure_id = f"{current_user()['username']}-{name}-{level}"
            student_adventure = g_db().student_adventure_by_id(student_adventure_id)
            if user_programs[level][name].submitted:
                adventure['state'] = 'submitted'
            if student_adventure and student_adventure['ticked']:
                adventure['state'] = 'ticked'

    return all_adventures


def unique_adventures_list(adventures_by_level):
    """
    Given a dict {level: [adventure_dict, ...]}, return a list of unique dicts
    with keys 'short_name' and 'name' for each unique short_name.
    """
    seen = set()
    result = []
    for level_adventures in adventures_by_level.values():
        for adv in level_adventures:
            sn = adv['short_name']
            if sn not in seen:
                seen.add(sn)
                result.append({'short_name': sn, 'name': adv['name']})
    result.sort(key=lambda x: x['name'].lower())
    return result
