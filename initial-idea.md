INITIAL IDEA
Ok, let's imagine one stable system prompt assistant from a UX perspective.
The interface is a page with: 
- a text input box where you write a sentence in japanese (required);
- two optional ones where you write — in any language — the intended meaning, and contextual info;
- radio buttons for the tone (business formal, formal, warm keigo, casual, slang, LINE),
- the results.
When you send the input, it first checks for obvious typos (lightest LLM), and if it finds one, aborts and displays "That seems wrong. Did you mean: `...`?".
If there's no typo, then another economical LLM checks the input's meaning.
if intended meaning was provided: 
- checks the input's meaning aganinst the intended meaning;
- if it matches, displays the full results;
- if not, displays "the sentence you provided means '...', as opposed to '...'. (two buttons: "analyze it anyway", "edit sentence")
If not provided, displays a list of possible meanings (if more than one interpretation is possible), letting you either pick one to continue the analysis, or go back to edit your sentence.
The final analysis will be a table with:
- sentence meaning,
- grammatical accuracy check,
- vocabulary accuracy check,
- naturalness check.