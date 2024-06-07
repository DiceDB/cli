# How to Catch Up with Latest Redis-doc

1. `git pull` in submodule.
2. Overwrite `diceroll/data/commands.json`.
3. Diff with old `commands.json`, make the changes.
4. `mv redis-doc/commands/*.md diceroll/data/commands`
5. `prettier --write --prose-wrap always diceroll/data/commands/*.md`

Done!
