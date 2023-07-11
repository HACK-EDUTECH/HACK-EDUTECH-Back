from typing import List
import json

class Senario:
    # system_content
    system_content: str = """Write a senario for middle school stduents with following [details]
    """

    situation: str = ""
    grammar: List[str] = [""]
    expression: List[str] = [""]
    word: List[str] = [""]
    partner: str = ""
    
    result_format: str = json.dumps({
        "title": "",
        "scene": "",
        "dialogue": [
            {
                "I": "",
                "Partner": "",
                "image_prompt": "",
            }
        ],
    })

    def __init__(self, situation: str, grammar: List[str], expression: List[str], word: List[str], partner: str) -> None:
        self.situation = situation
        self.grammar = grammar
        self.expression = expression
        self.word = word
        self.partner = partner

    def get_system_content(self) -> str:
        return self.system_content

    def get_user_content(self) -> str:
        return "[format:json string] " + self.result_format + f"""
[details]
1. situation : {self.situation}
2. character : "I", [Partner:{self.partner}]
3. grammar : {", ".join(self.grammar)}
4. expression : {", ".join(self.expression)}
5. word: {", ".join(self.word)}
6. level : A2 - Elementary English
Instructions for Script 
1. scene : write a 1 simple sentence describing the situation; create [image_prompt] about the place in the scene
2. dialogue : write dialogue sentences between "I" and [Partner:{self.partner}] using all the words and expressions; 1 short sentence by the number of words; create a [image_prompt] describing the subject of the dialogue for every two sentences 
3. Make sure every [image_prompt] must contain following phrase "4K HD, neutral, flat"; do not include images of humans, animals, letters, words, text, sexual and violent content.
"""
