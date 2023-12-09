#!/bin/bash
diff -c <(jq --sort-keys . items.bak.json) <(jq --sort-keys . items.json)
