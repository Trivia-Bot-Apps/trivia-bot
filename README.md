# Trivia Bot

![Maintenance](https://img.shields.io/maintenance/yes/2020)
[![Discord Bots](https://top.gg/api/widget/status/715047504126804000.svg)](https://top.gg/bot/715047504126804000)
[![Discord Bots](https://top.gg/api/widget/upvotes/715047504126804000.svg)](https://top.gg/bot/715047504126804000)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6f42c1.svg)](http://makeapullrequest.com)
![CircleCi](https://circleci.com/gh/gubareve/trivia-bot.svg?style=svg)
![Syntax Check](https://github.com/gubareve/trivia-bot/workflows/Syntax%20Check/badge.svg)
[![Build Status](https://dev.azure.com/evchik2007/com.kd7t.triviabot/_apis/build/status/gubareve.trivia-bot?branchName=master)](https://dev.azure.com/evchik2007/com.kd7t.triviabot/_build/latest?definitionId=1&branchName=master)

  
## [Invite Link:](https://discord.com/api/oauth2/authorize?client_id=715047504126804000&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D715047504126804000%26scope%3Dbot%26permissions%3D537263168&response_type=code&scope=identify)  

A easy to use multiple choice and true/false trivia bot for discord the includes a global leaderboard, categories, server leaderboards, and a infinite amount of control. **You can use the code if you credit us, by the original creators discretion.**

## Getting Started:

Simply do `docker run --env bottoken=YOURTOKENHERE --env REDIS_URL=YOURREDISHERE -env kd7t/triviabot`

## Commands:

NOTE: ignore the [ ] that just shows what should be there when entering the command

```
;vote
;trivia [optional category] - Play trivia
;multichoice [optional category] - Play multiple choice trivia
;truefalse [optional category] - Play true/false trivia
;categories - Lists categories
;top - Lists top players
;points - Lists your points
;servertop - Lists top users in your server
;invite - Pastes invite link
;credits - Shows credits
;ping - Shows ping
;version - Shows version info (Heroku Only)
```

## Admin Panel:

Admins have access to the admin panel:

![Admin Panel](https://raw.githubusercontent.com/gubareve/trivia-bot/master/images/Screen%20Shot%202020-06-13%20at%207.55.01%20PM.png)

Note: The file name is ```admin.py```

Also Note: To access the admin panel the REDIS URL and the token must be provided.

## Admin Commands:

NOTE: these only work for admins (Everyone with the manage bot permission).

```
;triviadebug - This is echos the contents of the data key (actually everyone can use it but its useless)
;servers - This lists the servers the bot is in.
;setplaying - Sets the "Playing" messages
;run - Executes python command
```

## TO DO:

* Point Streaks

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://kd7t.com"><img src="https://avatars3.githubusercontent.com/u/24500411?v=4" width="100px;" alt=""/><br /><sub><b>Evan Gubarev</b></sub></a><br /><a href="https://github.com/gubareve/trivia-bot/commits?author=gubareve" title="Code">💻</a> <a href="#design-gubareve" title="Design">🎨</a> <a href="#ideas-gubareve" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-gubareve" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://github.com/WickedTree"><img src="https://avatars0.githubusercontent.com/u/50127946?v=4" width="100px;" alt=""/><br /><sub><b>WickedTree Development</b></sub></a><br /><a href="#design-WickedTree" title="Design">🎨</a> <a href="https://github.com/gubareve/trivia-bot/commits?author=WickedTree" title="Code">💻</a></td>
    <td align="center"><a href="http://persistentbits.com"><img src="https://avatars0.githubusercontent.com/u/49598383?v=4" width="100px;" alt=""/><br /><sub><b>thexpiredpear</b></sub></a><br /><a href="https://github.com/gubareve/trivia-bot/commits?author=thexpiredpear" title="Code">💻</a> <a href="#design-thexpiredpear" title="Design">🎨</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Images:

![A multi question](https://raw.githubusercontent.com/gubareve/trivia-bot/master/images/Screen%20Shot%202020-06-18%20at%2012.38.47%20AM.png)

![A sample question](https://raw.githubusercontent.com/gubareve/trivia-bot/master/images/Screen%20Shot%202020-06-08%20at%209.06.00%20PM.png)

![Global Leaderboards](https://raw.githubusercontent.com/gubareve/trivia-bot/master/images/Screen%20Shot%202020-05-27%20at%2012.34.32%20PM.png)

![Personal Points](https://raw.githubusercontent.com/gubareve/trivia-bot/master/images/Screen%20Shot%202020-05-27%20at%2012.34.46%20PM.png)

## Copyright

(c) 2020 [KD7T Enterprises](https://github.com/gubareve)
