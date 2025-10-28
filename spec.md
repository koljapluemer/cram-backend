Build out a basic MVP based on this generated Django projects.

Put global settings in `./config/`, but everything else in `./main/`

For now, let's just build models and an admin view (just for all the models).

We need:

## Language

- 639 ISO language code (soo just a `string`); field name `code`
- name: `string`

## LanguageString

- a helper model with just two fields, `language` (ref to `Language`) easy and a string `content` 

## Situation

- `descriptions`: `LanguageString[]`
- `image_url`? Optional URL

## Communication

- `situations`
- `content`: `LanguageString`

## Prompts

- `situations` (many2many `Situation`)
- `descriptions`: `LanguageString[]`

## Context

- `contextType`: string
- `content`: string

## Utterance

- belongs to exactly one `communication`
- `transliteration`? : string
- `contexts`: `Context[]` (each context belongs to exactly one utterance)

## Clarification Questions

1. For `LanguageString`, should `content` support rich text/HTML or remain plain text, and do we need to enforce a specific max length?

plaintext, nothing special

2. Should `Situation.image_url` allow multiple URLs, and are there storage or validation rules (e.g., S3 paths vs. public URLs)?

was a typo, only single url, no validation

3. For `Context.contextType`, do we have a controlled vocabulary or enum to model, and if so where is it defined?

for now, contextType is plaintext
