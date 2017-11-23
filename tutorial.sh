#!/usr/bin/env sh
./playgame.py --map_file maps/example/tutorial1.map --log_dir game_logs --turns 60 --scenario --food none --player_seed 7 --verbose -e "$@" \
	"python player_bots/amazingRLbot.py" \
	"python sample_bots/python/HunterBot.py" 
