# Markov chiain impersonation bot

## Markov chain bot using
**markovify** or **Self-developed package**

 1.get_data_from_slack.py script lets the user get channel specfic data and individual specific data from slack

 2.package_everyone_slack_channels_bot.py lets lets the bot moniter conversation on slack and post messags, update databases. (Using Markovify package)
 
 2.vanilla_everyone_slack_channels_bot.py lets lets the bot moniter conversation on slack and post messags, update databases.
 (Using a self-developed package)

custom_markov.py is devopled by myself, each word is a state. The next word only depends on the current word. 

The code framework is inspired by [Loftylab](https://hirelofty.com/blog/how-build-slack-bot-mimics-your-colleague/). However, I developed my own markov chain package to compare with **markovify**. 
