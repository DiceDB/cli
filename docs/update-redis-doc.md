# How to Catch Up with Latest Redis-doc

1. `git pull` in submodule.
2. Overwrite `dice/data/commands.json`.
3. Diff with old `commands.json`, make the changes.
4. `mv redis-doc/commands/*.md dice/data/commands`
5. `prettier --write --prose-wrap always dice/data/commands/*.md`

Done!
