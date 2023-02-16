# A Discord Bot Dedicated to Ben Xu
 Xu Yu Jia (B哥）YYDS

It's recommended to use `JetBrains PyCharm` for the development work of this bot. `Poetry` is the dependency managment system used for this project.

A brief overview on the existing codebase inside `src` folder
- `constants.py`: it stores static, final variables such as the `channel_id` of the general text channel, the `user_id` of Ben Xu, the trigger words, etc. A lot of contents in this file will be replaced by a `sql` database in the near future.
- `bot.py`: the main bot life-cycles and functions. Please refer to the [discord.py](https://discordpy.readthedocs.io/en/stable/) for specific function documentations. Note that the `API KEY` is stored using `.env` file and not committed to Github. If you want to modify the code, please request this file from [@listar2000](https://github.com/listar2000).
- `main.py` is a simple entrance interface to run the bot.

### TODOS
- [ ] Custom response phrases and trigger keywords (require DB support)
- [ ] Deploy on Heroku
- [ ] Better streaming notification
- [ ] Dedicated League status for `bilibilifungame`
