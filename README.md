[日本語](README.md) | [English](README.en.md)

# slack-archive-reminder

Slack でしばらく使われていないチャンネルに対してアーカイブを促すメッセージを送るためのスクリプトです。

![slack-archive-reminder.png](slack-archive-reminder.png)

# How to use

## Create Your Slack App

https://api.slack.com/apps へアクセスし、 `Create New App` から新規アプリを _scratch_ で作成してください。  
※もちろん既存のAppを使っても問題ありません  

作成した App にて
 - Basic Infomation -> Display Information -> App Name, Short Descrioption, Backgroud color を任意の内容で設定してください。  
 - OAuth & Permissions -> Scopes より、以下の Scope を設定してください
   - Bot Token Scopes
     - chat:write
     - chat:write.public
   - User Token Scopes
     - channels:history
     - channels:read
     - groups:history
     - groups:read

上記が完了したら、利用したいワークスペースに App をインストールしてください。User OAuth Token と Bot User OAuth Token が生成されます。この内容を控えてください。  

## Set this repo to your server

### prepare

このリポジトリを使用したいサーバにインストールしてください。  
```
$ git clone https://github.com/mollinaca/slack-archive-reminder.git
$ cd slack-archive-reminder
```

config.ini を作成し編集してください。
```
$ cp config.ini.example config.ini
```

### config.ini の内容について

exampleファイルの中には以下のように記載されています。
```
[slack]
user_token=xoxp-<YOUR_SLACK_USER_TOKEN>
bot_token=xoxb-<YOUR_SLACK_BOT_TOKEN>
threshold = 2592000  # [sec], 2592000 sec means 30 days
exclude_list = ['general','random']
debug_channel = xxxxxxxx
bot_message = Hi, I'm slack-archive-reminder.
    It seems that this channel has not been used for some time.
    If you will not be using it in the future, consider archiving this channel.
    How to ? -> https://slack.com/help/articles/213185307

```
 - *user_token* に Slack APP の User OAuth Token を設定してください
 - *bot_token* に Slack APP の Bot User OAuth Token を設定してください
 - *threshold* に 「この秒数より長い期間発言がなかったらリマインドを送る」しきい値を設定してください。デフォルトでは _259200_ となっています。これは30日間を意味します。
 - *exclude_list* に、リマインド対象から除外したいチャンネル名を記載してください。対象がない場合は空のリスト [] としてください。
 - *debug_channel* は、もし動作確認を事前に行いたければ、発言されても問題ないチャンネルのIDを指定してください。この内容を設定し、 _main.py_ の内部で設定されている `DEBUG` 変数を _True_ に設定すると、アーカイブを促すメッセージを _debug_channel_ で指定されたチャンネルにポストします。
 - *bot_message* には、アーカイブを促すための（もしくはチャンネルにポストしたい）メッセージを設定してください。デフォルトのままで問題なければそのまま使ってください。


### pip install or pipenv shell

このスクリプトでは pip module である python-slack-sdk を使用します。
以下の手順でインストールしてください。

```
$ pip install slack_sdk
```
pipenv が有効な環境であれば、同梱されている `Pipfile` により実行されます。  
なお、pipenv では python のバージョン `3.9.6` で動作確認しています。  
```
$ pipenv shell
Launching subshell in virtual environment…
 . /root/.local/share/virtualenvs/slack-archive-reminder-nUILTd8E/bin/activate

$ python --version
Python 3.9.6
(slack-archive-reminder)
```

### Run

`main.py` を実行してください。  
SlackAPI実行時にエラーが発生した場合、標準エラー出力にエラーの内容を出力して終了します。エラー内容については Slack API のドキュメントを参照してください。  

_cron_ 等を用いて定期実行することも可能です。  


# refs

https://github.com/slackapi/python-slack-sdk  
https://api.slack.com/methods/conversations.list  
https://api.slack.com/methods/conversations.history  
https://api.slack.com/methods/chat.postMessage  
