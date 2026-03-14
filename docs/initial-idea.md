# PROOF OF CONCEPT

## Tone analysis overview

Ok, let's imagine one stable system prompt assistant from a UX perspective.

The interface is a page with: 
- a text input box where you write a sentence in japanese (required);
- two optional ones where you write — in any language — the intended meaning, and contextual info;
- radio buttons for the tone (business formal, formal, warm keigo, casual, slang, LINE),
- the results.

When you send the input, it first checks for obvious typos (lightest LLM), and if it finds one, aborts and displays "That seems like a typo. Did you mean: `...`?".
If there's no typo, then another economical LLM checks the input's meaning.

If intended meaning was provided: 
- checks the input's meaning aganinst the intended meaning;
- if it matches, displays the full results;
- if not, displays "the sentence you provided means '...', as opposed to '...'. (two buttons: "analyze it anyway", "edit sentence")
If not provided, displays a list of possible meanings (if more than one interpretation is possible), letting you either pick one to continue the analysis, or go back to edit your sentence.

The final analysis will be a table with:
- sentence meaning,
- grammatical accuracy check,
- vocabulary accuracy check,
- naturalness check.

## API calls

### Typo check

**Model:**  
Ministral 8B

**System instructions:**  
```
You are a Japanese typo checker. Check if the user's Japanese sentence contains obvious typos (wrong kana, common mistakes), and return your evaluation:

- sentence is fine = return "ok",
- obvious typo/miss = return "typo" (along with a corrected version),
- sentence is in japanese but incomprehensible = return "nonsense",
- sentence is not in japanese at all = return "foreign". 
```
**Schema:**
```json
{
  "type": "object",
  "properties": {
    "evaluation": {
      "type": "string",
      "enum": ["ok", "typo", "nonsense", "foreign"]
    },
    "correction": {
      "type": "string",
      "description": "Corrected version if typo detected, null otherwise",
      "nullable": true
    }
  },
  "required": [
    "evaluation", "correction"
  ]
}
```

### Meaning check (Didn't work, and maybe no need!)

**Model:**  
Gemini Flash Lite 2.5

**System instructions:**  
```
You are a Japanese translator. Analyze the user's Japanese sentence and provide possible English interpretations.

If the sentence has only one clear meaning, return a single interpretation with high confidence.
Only return multiple interpretations if the Japanese sentence is genuinely ambiguous (e.g., different grammatical interpretations, homonyms, context-dependent meanings).
Do NOT return multiple entries just because there are different ways to phrase the same meaning in English.

Consider the provided tone and context when interpreting.
```
**Schema:**
```json
{
  "type": "object",
  "properties": {
    "possible_meanings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "meaning": {
            "type": "string",
            "description": "English translation/interpretation"
          },
          "plausibility": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "description": "How plausible it is for the user input to mean this"
          }
        },
        "required": ["meaning", "plausibility"]
      }
    }
  },
  "required": ["possible_meanings"]
}
```

### Meaning cross reference

**Model:**  
Mistral Small

**System instructions:**  
```
You are a Japanese translator. The user will provide a sentence in Japanese and its intended meaning in English.

Interpret the Japanese sentence and check whether your interpretation semantically matches the user's intended meaning.
Set "matches" to true if the meanings match, even if:
- they match loosely (e.g.: "イスタンブールから飛行機で到着した = "I flew back from Istanbul"),
- the wording is not natural,
- there are grammar/vocabulary mistakes.
Set "matches" to false only if the provided sentence CAN NOT be interpreted as the intended meaning (wrong subject, tense, action, etc.).

Consider the provided tone and context when interpreting.
```
**Schema:**
```json
{
    "type": "object",
    "properties": {
        "interpretation": {
            "type": "string",
            "description": "Your interpretation of the user's Japanese sentence, in English"
        },
        "matches": {
            "type": "boolean",
            "description": "Whether your interpretation matches the intended meaning provided by the user"
        }
    },
    "required": ["interpretation", "matches"]
}
```

### Full analysis

**Model:**
Mistral Large

System instructions and schema are saved in different files.  
