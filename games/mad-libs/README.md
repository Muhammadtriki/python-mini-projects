# Mad Libs

Pick a story, answer the prompts, and read the funny result with a typewriter effect.

```
python mad_libs.py
```

Three stories are included: Space Adventure, Fairy Tale and Detective Story. Blank answers are not accepted, and prompts that ask for a number only accept digits.

## Add your own story

Stories live in `stories.json`. Give a story a title, a template with `{placeholders}`, and one prompt per placeholder:

```json
{
  "My Story": {
    "template": "Today {name} found a {adjective} {noun}.",
    "prompts": {
      "name": "Enter a name",
      "adjective": "Enter an adjective",
      "noun": "Enter a noun"
    }
  }
}
```

A placeholder can appear more than once in the template and is only asked for once. When the game starts it checks that every placeholder has a prompt, so a typo shows up immediately instead of halfway through a story.

## Options

`TYPING_DELAY` at the top of `mad_libs.py` sets the typewriter speed. Set it to `0` for instant output.
