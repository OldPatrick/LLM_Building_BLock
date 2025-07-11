# LLM_Building_BLock

01 - Shows usage of classes for LLM schemas, to get structured Output for further Models or processes of Workflows or Agents <br>
02 - Shows conversaTIONS within LLM (and potentially cross LLM), to correct a firewall missclassification of one LLM (4o-mini) through another LLM (claude haiku) <br>
03 - Shows a summary function, where we can get a structured output of pros and cons of a review <br>
04 - utomates 03 by pasting a url, and stripping tags from the parsed text to reduce token budget <br>
05 - shows the use of different LLMs to forecast spam, while using a cache class to store results locally in a SQLite DB.
It further shows that different models (and if the user wants to) different prompts lead to different results.
However, changing between providers needs rework of the approach and/or a unified schema, tests in the notebook before show, that would need a little more work.