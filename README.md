# Tweets-To-Text

TweetsToText is a bot that lives on Twitter. It collects your tweets into plain text files. So you can take your brilliant observations somewhere else.

[![Build Status](https://travis-ci.com/rji-futures-lab/tweets-to-text.svg?branch=master)](https://travis-ci.com/rji-futures-lab/tweets-to-text)
[![Coverage Status](https://coveralls.io/repos/github/rji-futures-lab/tweets-to-text/badge.svg?branch=master)](https://coveralls.io/github/rji-futures-lab/tweets-to-text?branch=master)

## How it works:

1. Follow [@TweetsToText](https://twitter.com/TweetsToText). It sends you a welcoming direct message.
2. Mention @TweetsToText before you start tweet-stormin'.
3. Mention @TweetsToText again in your final tweet.
4. Check your DMs. @TweetsToText will send you a link where you can download your text file.
5. Do whatever. You can copy and paste the text into your favorite text editor or your CMS, or share the link (which is public) with your editor or whoever).

## Development notes

TweetsToText is built atop Twitter's [Account Activity API](https://developer.twitter.com/en/docs/accounts-and-users/subscribe-account-activity/overview), which is designed for receiving and responding to events such as direct messages and account mentions on Twitter.

The deployed instance is subscribed to activity on the TweetsToText Twitter account. However, when working on improvements to the app, we need to avoid any disruptions for our actual users. Therefore, local instances of the app will subscribe to a [separate testing account](https://twitter.com/T2Tproto).

In order to subscribe to account activity, we must register a webhook: A url at which our app can receive messages from Twitter. We can use [ngrok](https://ngrok.com/) to expose our localhost server to the public internet with HTTPS.

So if you haven't already, [download](https://ngrok.com/download) and install ngrok.

Navigate into the tweets-to-text project directory, activate your virtual environment, and start the local server:

```sh
python manage.py runserver
```

Now open a separate terminal window (or tab), and start ngrok:

```sh
ngrok http 8000
```

Now we have a tunnel from the public internet to our local server. We can test this by copying the url in ngrok's output that looks like `https://{random characters}.ngrok.io`, and pasting this into web browser address bar. We should see the homepage for TweetsToText.

Finally, we have to register a webhook under the temporary domain generated by ngrok. At this point we need to open *yet another terminal window (or tab)* because we have to leave both the local webserver and ngrok running.

Navigate into the tweets-to-text project directory, activate your virtual environment, and call this handy management command with the temporary ngrok domain:

```sh
python manage.py replacewebhook '{random characters}.ngrok.io'
```

Hopefully the output of the management command will indicate, and now you can start working on improvments to TweetsToText.

## Deployment notes

TweetsToText takes advantage of Travis CI's continuous integration and automation features for deployment. When changes to the project are pushed to the master branch, Travis automatically attemtps to build and test the code. If all of the tests pass, Travis will call:

```sh
zappa update prod
```

The project should deploy successfully, using encrypted versions of the `zappa_settings.json` and `secrets.cfg` files stored in the repo.

#### Updating `zappa_settings.json` or `secrets.cfg`

If changes need to be made to either the `zappa_settings.json` or `secrets.cfg` file, we must re-encrypt the files and push the updated versions to the repo. To do this, we first must remove the `profile_name` entry from the `zappa_settings.json` file to ensure Zappa looks for environment variables instead of `~/.aws/credentials`. 

Next, remove the current `secrets.tar.enc` file with `rm secrets.tar.enc`. Then an archive of the `zappa_settings.json` and `secrets.cfg` files must be created:

```sh
tar cvf secrets.tar zappa_settings.json secrets.cfg
```

We then must encrypt the new `secrets.tar` file and then remove the unencrypted `secrets.tar` file from our directory:

```sh
travis encrypt-file secrets.tar --add --pro
rm secrets.tar
```

The `--add` argument should automatically update the `travis.yml` file with instructions for decrypting the new secrets.tar file. The `before_install` part of the `travis.yml` file should now look something like this:

```sh
before_install:
- openssl aes-256-cbc -K $encrypted_[…]_key -iv $encrypted_[…]_iv
 -in secrets.tar.enc -out secrets.tar -d
- tar xvf secrets.tar
```

If there are multiple decryption commands, remove the old ones. Go ahead and undo the deletion of the `profile_name` entry from the `zappa_settings.json` file to allow local testing. Commit your new `secrets.tar.enc` file and updated `travis.yml` file and push to the master branch. The project should be ready for automatic deployment.

#### Updating AWS credentials

If changes need to be made to the AWS credentials for the project, we must re-encrypt the credentials as environment variables in the `travis.yml` file.

This is done with:

```sh
travis encrypt AWS_ACCESS_KEY_ID=[value] --add --pro
travis encrypt AWS_SECRET_ACCESS_KEY=[value] --add --pro
```

The `env` part of the `travis.yml` file should now look something like this:

```sh
env:
  global:
  - DJANGO_ENV=test
  - PIPENV_VERBOSITY=-1
  - secure: [encrypted key value]
  - secure: [encrypted key value]
```

Go ahead and commit your updated `travis.yml` file and push to master. The project should be ready for autmatic deployment.