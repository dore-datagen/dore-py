# Copyright 2022 Bhargav KN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Redis JSON Decoder
"""

import json
from datetime import datetime

class RedisJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self,
            object_hook=self.object_hook, *args, **kwargs
        )

    def object_hook(self, obj):
        for (key, value) in obj.items():
            try:
                obj[key] = datetime.fromisoformat(value)
            except (ValueError, AttributeError, TypeError):
                obj[key] = value
        return obj