# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import urllib
import eventlet

from mycroft_jarbas_utils.skills.auto_translatable import AutotranslatableFallback


class FallbackPersonaSkill(AutotranslatableFallback):
    def __init__(self):
        AutotranslatableFallback.__init__(self)
        self.persona_url = "http://training.mycroft.ai/persona/api/persona/?"
        self.input_lang = "en-us"

    def initialize(self):
        self.register_fallback(self.handle_fallback_persona, 8)

    def get_intro_message(self):
        name = "persona"
        return "you installed universal " + name + " skill, you should " \
               "also blacklist the official " + name + \
               " skill to avoid potential problems"

    def handle_fallback_persona(self, message):
        query = message.data['utterance']
        query_obj = {"query": query}
        url_encode = urllib.urlencode(query_obj)
        try:
            with eventlet.Timeout(3):
                response_obj = \
                    requests.get(self.persona_url + url_encode).json()
            if float(response_obj['confidence']) < 0.7:
                return False
            response = response_obj['response']
            self.speak(response)
            return True
        except:
            self.log.info("error in persona fallback request")
            return False


def create_skill():
    return FallbackPersonaSkill()
