# Voting-Discord-Bot

Install Python: https://www.python.org/downloads/

Refer to the `./src` for all relevant dependencies used in respective Python scripts.

Refer to example_token.env for setting up .env/environment variables for securing the Discord `BOT_TOKEN`.

Six JSON files are used in conjunction with this code to maintain a local database for all users, voting groups, and proposal voting records. They should all be created as empty files ({}):
- `user_database.json`: Discord User IDs/Usernames and on-chain verified wallets.
- `holder_database.json`: Dynamic on-chain data based on users' NFT holdings pulled each time a command is run.
- `creator_database.json`: Creator wallets with all relevant assets to be used in voting.
- `voting_group_database.json`: Created Voting Groups with parameters including voting requirements, voting weight, and excluded assets.
- `active_proposals.json`: Active proposals per Voting Group at any given time.
- `completed_proposals.json`: Completed proposals per Voting Group, accessible by all users at any time.

## Features

### Slash Commands

`/vb_create` allows users with a creator wallet to create a Voting Group setting voting requirements, voting weight, and excluded assets.

`/vb_vote` checks wallet holdings on-chain of user, cross-checks Voting Group database and allows user to vote on active proposals with holdings related to created Voting Groups

### Server Interoperability

The Discord bot will be available to all servers and allow users to create Voting Groups and vote from any server.

### Python 

Python (.py) files are developed in the `./src` directory.
