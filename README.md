# Cyan Telegram Bot

A Telegram permission control bot that turns off all permission except send text for the new members in the group.


## Getting Started

Set up the bot token in your however you want, for example:

`export TOKEN=YOURTOKEN`

Set up the MongoDB url, and set up your [MongoDB Server](https://docs.mongodb.com/manual/installation/)

`export DATABASE_URL=YOURURL`

Install the dependencies:

PS: Please note that this project is based on python3, please do not use python2  

`pip install -r requirements.txt` or `pip3 install -r requirements.txt`

Run the script:

`python -m cyan_telegram_moderator_bot` or `python3 -m cyan_telegram_moderator_bot`


## Details

When new user enters chat, the bot first ban all rights except 'Send Text'.

When any user send a new message, the bot will create the user's profile if not exists, and increment the user's message count.

When the user has reached the message threshold, regular user privileges will be given to that user. 

<!-- ### Prerequisites

Python3

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
``` -->

<!-- ## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project. -->

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
<!-- 
## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc -->
