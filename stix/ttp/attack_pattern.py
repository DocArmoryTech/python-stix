# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import stix

class AttackPattern(stix.Entity):
    def to_obj(self, return_obj=None):
        return None
    
    @classmethod
    def from_obj(cls, obj, return_obj=None):
        return None
    
    def to_dict(self):
        return {}
    
    @classmethod
    def from_dict(cls, dict_repr, return_obj=None):
        return None