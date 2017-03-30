from .base import Vocabulary
import re

_hcpcs_split_regex = re.compile('([A-z]*)([0-9]+)')
def ubrev_split(code):
    match = _hcpcs_split_regex.match(code)
    letter_part = match.groups()[0]
    number_part = match.groups()[1]
    return letter_part, number_part

def ubrev_join(letter_part, number_part):
    digits = 5 - len(letter_part)
    return letter_part + (('%%.%dd' % digits) % int(number_part))



class HCPCS(Vocabulary):
    @staticmethod
    def _fill_range(start, end):
        start_letter, start_number = ubrev_split(start)
        end_letter, end_number = ubrev_split(end)
        assert start_letter == end_letter
        result = []
        for num in range(int(start_number), int(end_number) + 1):
            result.append(ubrev_join(start_letter, num))
        return result
    
    @staticmethod
    def _match_pattern(pattern):
        return [pattern]
    
    @staticmethod
    def standardize(code):
        result = code.strip()
        assert len(result) == 5
        return result

class HCPCSModifier(Vocabulary):
    @staticmethod
    def _fill_range(start, end):
        return [start, end]
    
    @staticmethod
    def _match_pattern(pattern):
        return [pattern]
    
    @staticmethod
    def standardize(code):
        result = code.strip()
        assert len(result) == 2
        return result
    