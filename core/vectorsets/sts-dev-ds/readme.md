## Semantic textual similarity (sts) development set

The sentences in this dataset are sourced from `https://raw.githubusercontent.com/PhilipMay/stsb-multi-mt/main/data/stsb-en-dev.csv` and have been cleaned to remove quotes, duplicates, and other formatting issues.

Note: Source sentences have been converted to OpenAI embeddings (1536 dimensions)

```sh
# Sample entry where 'pg:sts' is vector set key and  's1' is element id (sentence id)
VADD 'pg:sts' 'VALUES' '1536' '-0.010130' '-0.026101'..... 's1' 'SETATTR' '{"sentence":"A young child is riding a horse.","activityType":"people","wordCount":7,"charCount":32}'
```
