from typing import List, Union, Dict


class Qbody:
    def __init__(self, stem: str, options: List = None, sub_qbody: List = None):
        self.stem = stem
        self.options = options if options else []
        self.sub_qbody = sub_qbody if sub_qbody else []

    def to_json(self):
        return {
            'stem': self.stem,
            'options': self.options,
            'sub_qbody': self.sub_qbody
        }

    def from_json(self, jd):
        self.stem = jd.get('stem', '')
        self.options = jd.get('options', [])
        self.sub_qbody = jd.get('sub_qbody', [])

