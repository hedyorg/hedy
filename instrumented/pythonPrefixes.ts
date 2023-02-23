function cov_18cxb3ee2g() {
  var path = "/home/capybara/repos/hedyc/static/js/pythonPrefixes.ts";
  var hash = "0e0c15c13e6743c181554fd467a75ab4be50e2ec";
  var global = new Function("return this")();
  var gcv = "__coverage__";
  var coverageData = {
    path: "/home/capybara/repos/hedyc/static/js/pythonPrefixes.ts",
    statementMap: {
      "0": {
        start: {
          line: 14,
          column: 0
        },
        end: {
          line: 28,
          column: 1
        }
      },
      "1": {
        start: {
          line: 31,
          column: 0
        },
        end: {
          line: 48,
          column: 1
        }
      },
      "2": {
        start: {
          line: 51,
          column: 0
        },
        end: {
          line: 148,
          column: 1
        }
      }
    },
    fnMap: {},
    branchMap: {},
    s: {
      "0": 0,
      "1": 0,
      "2": 0
    },
    f: {},
    b: {},
    _coverageSchema: "1a1c01bbd47fc00a2c39e90264f33305004495a9",
    hash: "0e0c15c13e6743c181554fd467a75ab4be50e2ec"
  };
  var coverage = global[gcv] || (global[gcv] = {});
  if (!coverage[path] || coverage[path].hash !== hash) {
    coverage[path] = coverageData;
  }
  var actualCoverage = coverage[path];
  {
    // @ts-ignore
    cov_18cxb3ee2g = function () {
      return actualCoverage;
    };
  }
  return actualCoverage;
}
cov_18cxb3ee2g();
/*******************************************************************************
*
* !!! THIS FILE HAS BEEN GENERATED. DO NOT EDIT !!!
*
* Make desired changes to prefixes/{normal,pygame,turtle}.py
*
* Add/edit tests for those changes in tests/test_python_prefixes.py
*
* Run build-tools/heroku/generate-prefixes-ts to regenerate.
*
*******************************************************************************/

export const turtle_prefix = (cov_18cxb3ee2g().s[0]++, `# coding=utf8

import random  # noqa F401
import time  # noqa F401
import turtle

t = turtle.Turtle()
t.shape("turtle")
t.hideturtle()
t.penup()
t.left(90)
t.pendown()
t.speed(3)
t.showturtle()
`);
export const pygame_prefix = (cov_18cxb3ee2g().s[1]++, `# coding=utf8

import pygame  # noqa F401
import buttons  # noqa F401

pygame.init()
canvas = pygame.display.set_mode((711, 300))
canvas.fill(pygame.Color(247, 250, 252, 255))

pygame_end = False
button_list = []


def create_button(name):
    if name not in button_list:
        button_list.append(name)
        buttons.add(name)
`);
export const normal_prefix = (cov_18cxb3ee2g().s[2]++, `# coding=utf8

import random  # noqa F401
import time  # noqa F401

try:
    import extensions  # noqa F401
except ModuleNotFoundError:
    # This is done because 'extensions' is not a python module but rather a Skulpt JS extension
    # These functions are defined in skulpt-stdlib-extensions.js
    # When running tests in test_python_prefixes it wil raise ModuleNotFoundError
    pass

global int_saver
global convert_numerals  # needed for recursion to work
int_saver = int


def int(s):
    if isinstance(s, str):
        numerals_dict = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8',
                         '9': '9', '𑁦': '0', '𑁧': '1', '𑁨': '2', '𑁩': '3', '𑁪': '4', '𑁫': '5', '𑁬': '6', '𑁭': '7',
                         '𑁮': '8', '𑁯': '9', '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6',
                         '७': '7', '८': '8', '९': '9', '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4', '૫': '5',
                         '૬': '6', '૭': '7', '૮': '8', '૯': '9', '੦': '0', '੧': '1', '੨': '2', '੩': '3', '੪': '4',
                         '੫': '5', '੬': '6', '੭': '7', '੮': '8', '੯': '9', '০': '0', '১': '1', '২': '2', '৩': '3',
                         '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9', '೦': '0', '೧': '1', '೨': '2',
                         '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9', '୦': '0', '୧': '1',
                         '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8', '୯': '9', '൦': '0',
                         '൧': '1', '൨': '2', '൩': '3', '൪': '4', '൫': '5', '൬': '6', '൭': '7', '൮': '8', '൯': '9',
                         '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8',
                         '௯': '9', '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7',
                         '౮': '8', '౯': '9', '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4', '၅': '5', '၆': '6',
                         '၇': '7', '၈': '8', '၉': '9', '༠': '0', '༡': '1', '༢': '2', '༣': '3', '༤': '4', '༥': '5',
                         '༦': '6', '༧': '7', '༨': '8', '༩': '9', '᠐': '0', '᠑': '1', '᠒': '2', '᠓': '3', '᠔': '4',
                         '᠕': '5', '᠖': '6', '᠗': '7', '᠘': '8', '᠙': '9', '០': '0', '១': '1', '២': '2', '៣': '3',
                         '៤': '4', '៥': '5', '៦': '6', '៧': '7', '៨': '8', '៩': '9', '๐': '0', '๑': '1', '๒': '2',
                         '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9', '໐': '0', '໑': '1',
                         '໒': '2', '໓': '3', '໔': '4', '໕': '5', '໖': '6', '໗': '7', '໘': '8', '໙': '9', '꧐': '0',
                         '꧑': '1', '꧒': '2', '꧓': '3', '꧔': '4', '꧕': '5', '꧖': '6', '꧗': '7', '꧘': '8', '꧙': '9',
                         '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8',
                         '٩': '9', '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7',
                         '۸': '8', '۹': '9', '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6',
                         '七': '7', '八': '8', '九': '9', '零': '0'}
        latin_numerals = ''.join([numerals_dict.get(letter, letter) for letter in s])
        return int_saver(latin_numerals)
    return (int_saver(s))


def convert_numerals(alphabet, number):
    numerals_dict_return = {
        'Latin': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        'Brahmi': ['𑁦', '𑁧', '𑁨', '𑁩', '𑁪', '𑁫', '𑁬', '𑁭', '𑁮', '𑁯'],
        'Devanagari': ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
        'Gujarati': ['૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯'],
        'Gurmukhi': ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯'],
        'Bengali': ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'],
        'Kannada': ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'],
        'Odia': ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯'],
        'Malayalam': ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯'],
        'Tamil': ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯'],
        'Telugu': ['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'],
        'Burmese': ['၀', '၁', '၂', '၃', '၄', '၅', '၆', '၇', '၈', '၉'],
        'Tibetan': ['༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩'],
        'Mongolian': ['᠐', '᠑', '᠒', '᠓', '᠔', '᠕', '᠖', '᠗', '᠘', '᠙'],
        'Khmer': ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩'],
        'Thai': ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙'],
        'Lao': ['໐', '໑', '໒', '໓', '໔', '໕', '໖', '໗', '໘', '໙'],
        'Javanese': ['꧐', '꧑', '꧒', '꧓', '꧔', '꧕', '꧖', '꧗', '꧘', '꧙'],
        'Arabic': ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'],
        'Persian': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'],
        'Urdu': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    }

    number = str(number)
    T = str

    sign = ''
    if number[0] == '-':
        sign = '-'
        number = number[1:]

    if number.replace('.', '', 1).isnumeric():
        numerals_list = numerals_dict_return[alphabet]
        if '.' in number:
            tokens = number.split('.')
            all_numerals_converted = [numerals_list[int(digit)] for digit in tokens[0]]
            all_numerals_converted.append('.')
            all_numerals_converted.extend(numerals_list[int(digit)] for digit in tokens[1])
            if alphabet == 'Latin':
                T = float
        else:
            all_numerals_converted = [numerals_list[int(digit)] for digit in number]
            if alphabet == 'Latin':
                T = int
        number = ''.join(all_numerals_converted)
    return T(f'{sign}{number}')
`);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjb3ZfMThjeGIzZWUyZyIsImFjdHVhbENvdmVyYWdlIiwidHVydGxlX3ByZWZpeCIsInMiLCJweWdhbWVfcHJlZml4Iiwibm9ybWFsX3ByZWZpeCJdLCJzb3VyY2VzIjpbInB5dGhvblByZWZpeGVzLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG4qXG4qICEhISBUSElTIEZJTEUgSEFTIEJFRU4gR0VORVJBVEVELiBETyBOT1QgRURJVCAhISFcbipcbiogTWFrZSBkZXNpcmVkIGNoYW5nZXMgdG8gcHJlZml4ZXMve25vcm1hbCxweWdhbWUsdHVydGxlfS5weVxuKlxuKiBBZGQvZWRpdCB0ZXN0cyBmb3IgdGhvc2UgY2hhbmdlcyBpbiB0ZXN0cy90ZXN0X3B5dGhvbl9wcmVmaXhlcy5weVxuKlxuKiBSdW4gYnVpbGQtdG9vbHMvaGVyb2t1L2dlbmVyYXRlLXByZWZpeGVzLXRzIHRvIHJlZ2VuZXJhdGUuXG4qXG4qKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG5leHBvcnQgY29uc3QgdHVydGxlX3ByZWZpeCA9IFxuYCMgY29kaW5nPXV0ZjhcblxuaW1wb3J0IHJhbmRvbSAgIyBub3FhIEY0MDFcbmltcG9ydCB0aW1lICAjIG5vcWEgRjQwMVxuaW1wb3J0IHR1cnRsZVxuXG50ID0gdHVydGxlLlR1cnRsZSgpXG50LnNoYXBlKFwidHVydGxlXCIpXG50LmhpZGV0dXJ0bGUoKVxudC5wZW51cCgpXG50LmxlZnQoOTApXG50LnBlbmRvd24oKVxudC5zcGVlZCgzKVxudC5zaG93dHVydGxlKClcbmA7XG5cbmV4cG9ydCBjb25zdCBweWdhbWVfcHJlZml4ID0gXG5gIyBjb2Rpbmc9dXRmOFxuXG5pbXBvcnQgcHlnYW1lICAjIG5vcWEgRjQwMVxuaW1wb3J0IGJ1dHRvbnMgICMgbm9xYSBGNDAxXG5cbnB5Z2FtZS5pbml0KClcbmNhbnZhcyA9IHB5Z2FtZS5kaXNwbGF5LnNldF9tb2RlKCg3MTEsIDMwMCkpXG5jYW52YXMuZmlsbChweWdhbWUuQ29sb3IoMjQ3LCAyNTAsIDI1MiwgMjU1KSlcblxucHlnYW1lX2VuZCA9IEZhbHNlXG5idXR0b25fbGlzdCA9IFtdXG5cblxuZGVmIGNyZWF0ZV9idXR0b24obmFtZSk6XG4gICAgaWYgbmFtZSBub3QgaW4gYnV0dG9uX2xpc3Q6XG4gICAgICAgIGJ1dHRvbl9saXN0LmFwcGVuZChuYW1lKVxuICAgICAgICBidXR0b25zLmFkZChuYW1lKVxuYDtcblxuZXhwb3J0IGNvbnN0IG5vcm1hbF9wcmVmaXggPSBcbmAjIGNvZGluZz11dGY4XG5cbmltcG9ydCByYW5kb20gICMgbm9xYSBGNDAxXG5pbXBvcnQgdGltZSAgIyBub3FhIEY0MDFcblxudHJ5OlxuICAgIGltcG9ydCBleHRlbnNpb25zICAjIG5vcWEgRjQwMVxuZXhjZXB0IE1vZHVsZU5vdEZvdW5kRXJyb3I6XG4gICAgIyBUaGlzIGlzIGRvbmUgYmVjYXVzZSAnZXh0ZW5zaW9ucycgaXMgbm90IGEgcHl0aG9uIG1vZHVsZSBidXQgcmF0aGVyIGEgU2t1bHB0IEpTIGV4dGVuc2lvblxuICAgICMgVGhlc2UgZnVuY3Rpb25zIGFyZSBkZWZpbmVkIGluIHNrdWxwdC1zdGRsaWItZXh0ZW5zaW9ucy5qc1xuICAgICMgV2hlbiBydW5uaW5nIHRlc3RzIGluIHRlc3RfcHl0aG9uX3ByZWZpeGVzIGl0IHdpbCByYWlzZSBNb2R1bGVOb3RGb3VuZEVycm9yXG4gICAgcGFzc1xuXG5nbG9iYWwgaW50X3NhdmVyXG5nbG9iYWwgY29udmVydF9udW1lcmFscyAgIyBuZWVkZWQgZm9yIHJlY3Vyc2lvbiB0byB3b3JrXG5pbnRfc2F2ZXIgPSBpbnRcblxuXG5kZWYgaW50KHMpOlxuICAgIGlmIGlzaW5zdGFuY2Uocywgc3RyKTpcbiAgICAgICAgbnVtZXJhbHNfZGljdCA9IHsnMCc6ICcwJywgJzEnOiAnMScsICcyJzogJzInLCAnMyc6ICczJywgJzQnOiAnNCcsICc1JzogJzUnLCAnNic6ICc2JywgJzcnOiAnNycsICc4JzogJzgnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICc5JzogJzknLCAn8JGBpic6ICcwJywgJ/CRgacnOiAnMScsICfwkYGoJzogJzInLCAn8JGBqSc6ICczJywgJ/CRgaonOiAnNCcsICfwkYGrJzogJzUnLCAn8JGBrCc6ICc2JywgJ/CRga0nOiAnNycsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ/CRga4nOiAnOCcsICfwkYGvJzogJzknLCAn4KWmJzogJzAnLCAn4KWnJzogJzEnLCAn4KWoJzogJzInLCAn4KWpJzogJzMnLCAn4KWqJzogJzQnLCAn4KWrJzogJzUnLCAn4KWsJzogJzYnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfgpa0nOiAnNycsICfgpa4nOiAnOCcsICfgpa8nOiAnOScsICfgq6YnOiAnMCcsICfgq6cnOiAnMScsICfgq6gnOiAnMicsICfgq6knOiAnMycsICfgq6onOiAnNCcsICfgq6snOiAnNScsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+CrrCc6ICc2JywgJ+CrrSc6ICc3JywgJ+Crric6ICc4JywgJ+Crryc6ICc5JywgJ+Cppic6ICcwJywgJ+Cppyc6ICcxJywgJ+CpqCc6ICcyJywgJ+CpqSc6ICczJywgJ+Cpqic6ICc0JyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAn4KmrJzogJzUnLCAn4KmsJzogJzYnLCAn4KmtJzogJzcnLCAn4KmuJzogJzgnLCAn4KmvJzogJzknLCAn4KemJzogJzAnLCAn4KenJzogJzEnLCAn4KeoJzogJzInLCAn4KepJzogJzMnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfgp6onOiAnNCcsICfgp6snOiAnNScsICfgp6wnOiAnNicsICfgp60nOiAnNycsICfgp64nOiAnOCcsICfgp68nOiAnOScsICfgs6YnOiAnMCcsICfgs6cnOiAnMScsICfgs6gnOiAnMicsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+CzqSc6ICczJywgJ+Czqic6ICc0JywgJ+Czqyc6ICc1JywgJ+CzrCc6ICc2JywgJ+CzrSc6ICc3JywgJ+Czric6ICc4JywgJ+Czryc6ICc5JywgJ+Ctpic6ICcwJywgJ+Ctpyc6ICcxJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAn4K2oJzogJzInLCAn4K2pJzogJzMnLCAn4K2qJzogJzQnLCAn4K2rJzogJzUnLCAn4K2sJzogJzYnLCAn4K2tJzogJzcnLCAn4K2uJzogJzgnLCAn4K2vJzogJzknLCAn4LWmJzogJzAnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfgtacnOiAnMScsICfgtagnOiAnMicsICfgtaknOiAnMycsICfgtaonOiAnNCcsICfgtasnOiAnNScsICfgtawnOiAnNicsICfgta0nOiAnNycsICfgta4nOiAnOCcsICfgta8nOiAnOScsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+Cvpic6ICcwJywgJ+Cvpyc6ICcxJywgJ+CvqCc6ICcyJywgJ+CvqSc6ICczJywgJ+Cvqic6ICc0JywgJ+Cvqyc6ICc1JywgJ+CvrCc6ICc2JywgJ+CvrSc6ICc3JywgJ+Cvric6ICc4JyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAn4K+vJzogJzknLCAn4LGmJzogJzAnLCAn4LGnJzogJzEnLCAn4LGoJzogJzInLCAn4LGpJzogJzMnLCAn4LGqJzogJzQnLCAn4LGrJzogJzUnLCAn4LGsJzogJzYnLCAn4LGtJzogJzcnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfgsa4nOiAnOCcsICfgsa8nOiAnOScsICfhgYAnOiAnMCcsICfhgYEnOiAnMScsICfhgYInOiAnMicsICfhgYMnOiAnMycsICfhgYQnOiAnNCcsICfhgYUnOiAnNScsICfhgYYnOiAnNicsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+GBhyc6ICc3JywgJ+GBiCc6ICc4JywgJ+GBiSc6ICc5JywgJ+C8oCc6ICcwJywgJ+C8oSc6ICcxJywgJ+C8oic6ICcyJywgJ+C8oyc6ICczJywgJ+C8pCc6ICc0JywgJ+C8pSc6ICc1JyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAn4LymJzogJzYnLCAn4LynJzogJzcnLCAn4LyoJzogJzgnLCAn4LypJzogJzknLCAn4aCQJzogJzAnLCAn4aCRJzogJzEnLCAn4aCSJzogJzInLCAn4aCTJzogJzMnLCAn4aCUJzogJzQnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfhoJUnOiAnNScsICfhoJYnOiAnNicsICfhoJcnOiAnNycsICfhoJgnOiAnOCcsICfhoJknOiAnOScsICfhn6AnOiAnMCcsICfhn6EnOiAnMScsICfhn6InOiAnMicsICfhn6MnOiAnMycsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+GfpCc6ICc0JywgJ+GfpSc6ICc1JywgJ+Gfpic6ICc2JywgJ+Gfpyc6ICc3JywgJ+GfqCc6ICc4JywgJ+GfqSc6ICc5JywgJ+C5kCc6ICcwJywgJ+C5kSc6ICcxJywgJ+C5kic6ICcyJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAn4LmTJzogJzMnLCAn4LmUJzogJzQnLCAn4LmVJzogJzUnLCAn4LmWJzogJzYnLCAn4LmXJzogJzcnLCAn4LmYJzogJzgnLCAn4LmZJzogJzknLCAn4LuQJzogJzAnLCAn4LuRJzogJzEnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfgu5InOiAnMicsICfgu5MnOiAnMycsICfgu5QnOiAnNCcsICfgu5UnOiAnNScsICfgu5YnOiAnNicsICfgu5cnOiAnNycsICfgu5gnOiAnOCcsICfgu5knOiAnOScsICfqp5AnOiAnMCcsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+qnkSc6ICcxJywgJ+qnkic6ICcyJywgJ+qnkyc6ICczJywgJ+qnlCc6ICc0JywgJ+qnlSc6ICc1JywgJ+qnlic6ICc2JywgJ+qnlyc6ICc3JywgJ+qnmCc6ICc4JywgJ+qnmSc6ICc5JyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAn2aAnOiAnMCcsICfZoSc6ICcxJywgJ9miJzogJzInLCAn2aMnOiAnMycsICfZpCc6ICc0JywgJ9mlJzogJzUnLCAn2aYnOiAnNicsICfZpyc6ICc3JywgJ9moJzogJzgnLFxuICAgICAgICAgICAgICAgICAgICAgICAgICfZqSc6ICc5JywgJ9uwJzogJzAnLCAn27EnOiAnMScsICfbsic6ICcyJywgJ9uzJzogJzMnLCAn27QnOiAnNCcsICfbtSc6ICc1JywgJ9u2JzogJzYnLCAn27cnOiAnNycsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ9u4JzogJzgnLCAn27knOiAnOScsICfjgIcnOiAnMCcsICfkuIAnOiAnMScsICfkuownOiAnMicsICfkuIknOiAnMycsICflm5snOiAnNCcsICfkupQnOiAnNScsICflha0nOiAnNicsXG4gICAgICAgICAgICAgICAgICAgICAgICAgJ+S4gyc6ICc3JywgJ+WFqyc6ICc4JywgJ+S5nSc6ICc5JywgJ+mbtic6ICcwJ31cbiAgICAgICAgbGF0aW5fbnVtZXJhbHMgPSAnJy5qb2luKFtudW1lcmFsc19kaWN0LmdldChsZXR0ZXIsIGxldHRlcikgZm9yIGxldHRlciBpbiBzXSlcbiAgICAgICAgcmV0dXJuIGludF9zYXZlcihsYXRpbl9udW1lcmFscylcbiAgICByZXR1cm4gKGludF9zYXZlcihzKSlcblxuXG5kZWYgY29udmVydF9udW1lcmFscyhhbHBoYWJldCwgbnVtYmVyKTpcbiAgICBudW1lcmFsc19kaWN0X3JldHVybiA9IHtcbiAgICAgICAgJ0xhdGluJzogWycwJywgJzEnLCAnMicsICczJywgJzQnLCAnNScsICc2JywgJzcnLCAnOCcsICc5J10sXG4gICAgICAgICdCcmFobWknOiBbJ/CRgaYnLCAn8JGBpycsICfwkYGoJywgJ/CRgaknLCAn8JGBqicsICfwkYGrJywgJ/CRgawnLCAn8JGBrScsICfwkYGuJywgJ/CRga8nXSxcbiAgICAgICAgJ0RldmFuYWdhcmknOiBbJ+ClpicsICfgpacnLCAn4KWoJywgJ+ClqScsICfgpaonLCAn4KWrJywgJ+ClrCcsICfgpa0nLCAn4KWuJywgJ+ClryddLFxuICAgICAgICAnR3VqYXJhdGknOiBbJ+CrpicsICfgq6cnLCAn4KuoJywgJ+CrqScsICfgq6onLCAn4KurJywgJ+CrrCcsICfgq60nLCAn4KuuJywgJ+CrryddLFxuICAgICAgICAnR3VybXVraGknOiBbJ+CppicsICfgqacnLCAn4KmoJywgJ+CpqScsICfgqaonLCAn4KmrJywgJ+CprCcsICfgqa0nLCAn4KmuJywgJ+CpryddLFxuICAgICAgICAnQmVuZ2FsaSc6IFsn4KemJywgJ+CnpycsICfgp6gnLCAn4KepJywgJ+CnqicsICfgp6snLCAn4KesJywgJ+CnrScsICfgp64nLCAn4KevJ10sXG4gICAgICAgICdLYW5uYWRhJzogWyfgs6YnLCAn4LOnJywgJ+CzqCcsICfgs6knLCAn4LOqJywgJ+CzqycsICfgs6wnLCAn4LOtJywgJ+CzricsICfgs68nXSxcbiAgICAgICAgJ09kaWEnOiBbJ+CtpicsICfgracnLCAn4K2oJywgJ+CtqScsICfgraonLCAn4K2rJywgJ+CtrCcsICfgra0nLCAn4K2uJywgJ+CtryddLFxuICAgICAgICAnTWFsYXlhbGFtJzogWyfgtaYnLCAn4LWnJywgJ+C1qCcsICfgtaknLCAn4LWqJywgJ+C1qycsICfgtawnLCAn4LWtJywgJ+C1ricsICfgta8nXSxcbiAgICAgICAgJ1RhbWlsJzogWyfgr6YnLCAn4K+nJywgJ+CvqCcsICfgr6knLCAn4K+qJywgJ+CvqycsICfgr6wnLCAn4K+tJywgJ+CvricsICfgr68nXSxcbiAgICAgICAgJ1RlbHVndSc6IFsn4LGmJywgJ+CxpycsICfgsagnLCAn4LGpJywgJ+CxqicsICfgsasnLCAn4LGsJywgJ+CxrScsICfgsa4nLCAn4LGvJ10sXG4gICAgICAgICdCdXJtZXNlJzogWyfhgYAnLCAn4YGBJywgJ+GBgicsICfhgYMnLCAn4YGEJywgJ+GBhScsICfhgYYnLCAn4YGHJywgJ+GBiCcsICfhgYknXSxcbiAgICAgICAgJ1RpYmV0YW4nOiBbJ+C8oCcsICfgvKEnLCAn4LyiJywgJ+C8oycsICfgvKQnLCAn4LylJywgJ+C8picsICfgvKcnLCAn4LyoJywgJ+C8qSddLFxuICAgICAgICAnTW9uZ29saWFuJzogWyfhoJAnLCAn4aCRJywgJ+GgkicsICfhoJMnLCAn4aCUJywgJ+GglScsICfhoJYnLCAn4aCXJywgJ+GgmCcsICfhoJknXSxcbiAgICAgICAgJ0tobWVyJzogWyfhn6AnLCAn4Z+hJywgJ+GfoicsICfhn6MnLCAn4Z+kJywgJ+GfpScsICfhn6YnLCAn4Z+nJywgJ+GfqCcsICfhn6knXSxcbiAgICAgICAgJ1RoYWknOiBbJ+C5kCcsICfguZEnLCAn4LmSJywgJ+C5kycsICfguZQnLCAn4LmVJywgJ+C5licsICfguZcnLCAn4LmYJywgJ+C5mSddLFxuICAgICAgICAnTGFvJzogWyfgu5AnLCAn4LuRJywgJ+C7kicsICfgu5MnLCAn4LuUJywgJ+C7lScsICfgu5YnLCAn4LuXJywgJ+C7mCcsICfgu5knXSxcbiAgICAgICAgJ0phdmFuZXNlJzogWyfqp5AnLCAn6qeRJywgJ+qnkicsICfqp5MnLCAn6qeUJywgJ+qnlScsICfqp5YnLCAn6qeXJywgJ+qnmCcsICfqp5knXSxcbiAgICAgICAgJ0FyYWJpYyc6IFsn2aAnLCAn2aEnLCAn2aInLCAn2aMnLCAn2aQnLCAn2aUnLCAn2aYnLCAn2acnLCAn2agnLCAn2aknXSxcbiAgICAgICAgJ1BlcnNpYW4nOiBbJ9uwJywgJ9uxJywgJ9uyJywgJ9uzJywgJ9u0JywgJ9u1JywgJ9u2JywgJ9u3JywgJ9u4JywgJ9u5J10sXG4gICAgICAgICdVcmR1JzogWyfbsCcsICfbsScsICfbsicsICfbsycsICfbtCcsICfbtScsICfbticsICfbtycsICfbuCcsICfbuSddXG4gICAgfVxuXG4gICAgbnVtYmVyID0gc3RyKG51bWJlcilcbiAgICBUID0gc3RyXG5cbiAgICBzaWduID0gJydcbiAgICBpZiBudW1iZXJbMF0gPT0gJy0nOlxuICAgICAgICBzaWduID0gJy0nXG4gICAgICAgIG51bWJlciA9IG51bWJlclsxOl1cblxuICAgIGlmIG51bWJlci5yZXBsYWNlKCcuJywgJycsIDEpLmlzbnVtZXJpYygpOlxuICAgICAgICBudW1lcmFsc19saXN0ID0gbnVtZXJhbHNfZGljdF9yZXR1cm5bYWxwaGFiZXRdXG4gICAgICAgIGlmICcuJyBpbiBudW1iZXI6XG4gICAgICAgICAgICB0b2tlbnMgPSBudW1iZXIuc3BsaXQoJy4nKVxuICAgICAgICAgICAgYWxsX251bWVyYWxzX2NvbnZlcnRlZCA9IFtudW1lcmFsc19saXN0W2ludChkaWdpdCldIGZvciBkaWdpdCBpbiB0b2tlbnNbMF1dXG4gICAgICAgICAgICBhbGxfbnVtZXJhbHNfY29udmVydGVkLmFwcGVuZCgnLicpXG4gICAgICAgICAgICBhbGxfbnVtZXJhbHNfY29udmVydGVkLmV4dGVuZChudW1lcmFsc19saXN0W2ludChkaWdpdCldIGZvciBkaWdpdCBpbiB0b2tlbnNbMV0pXG4gICAgICAgICAgICBpZiBhbHBoYWJldCA9PSAnTGF0aW4nOlxuICAgICAgICAgICAgICAgIFQgPSBmbG9hdFxuICAgICAgICBlbHNlOlxuICAgICAgICAgICAgYWxsX251bWVyYWxzX2NvbnZlcnRlZCA9IFtudW1lcmFsc19saXN0W2ludChkaWdpdCldIGZvciBkaWdpdCBpbiBudW1iZXJdXG4gICAgICAgICAgICBpZiBhbHBoYWJldCA9PSAnTGF0aW4nOlxuICAgICAgICAgICAgICAgIFQgPSBpbnRcbiAgICAgICAgbnVtYmVyID0gJycuam9pbihhbGxfbnVtZXJhbHNfY29udmVydGVkKVxuICAgIHJldHVybiBUKGYne3NpZ259e251bWJlcn0nKVxuYDtcbiJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0lBZVk7SUFBQUEsY0FBQSxZQUFBQSxDQUFBO01BQUEsT0FBQUMsY0FBQTtJQUFBO0VBQUE7RUFBQSxPQUFBQSxjQUFBO0FBQUE7QUFBQUQsY0FBQTtBQWZaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEsT0FBTyxNQUFNRSxhQUFhLElBQUFGLGNBQUEsR0FBQUcsQ0FBQSxPQUN6QjtBQUNEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQztBQUVELE9BQU8sTUFBTUMsYUFBYSxJQUFBSixjQUFBLEdBQUFHLENBQUEsT0FDekI7QUFDRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLENBQUM7QUFFRCxPQUFPLE1BQU1FLGFBQWEsSUFBQUwsY0FBQSxHQUFBRyxDQUFBLE9BQ3pCO0FBQ0Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQyJ9