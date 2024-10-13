# Perlin noise

## 参考リンク
- [パーリンノイズを理解する | POSTD](https://postd.cc/understanding-perlin-noise/)
- [パーリンノイズ｜クリエイティブコーディングの教科書](https://zenn.dev/baroqueengine/books/a19140f2d9fc1a/viewer/95c334)


## Windows 環境構築
### pyenv
PowerShell で以下のコマンドを実行する。

```
pip install pyenv-win --target $HOME\.pyenv
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```

PowerShell を再起動して以下のコマンドを実行する。

```
pyenv install 3.10.5
pyenv local 3.10.5
```

## poetry
PowerShell を再起動して以下のコマンドを実行する。

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

`%APPDATA%\Python\Scripts` にパスを通す。

PowerShell を再起動して以下のコマンドを実行する。

```
poetry env use "$env:HOMEDRIVE$env:HOMEPATH\.pyenv\pyenv-win\versions\3.10.5\python.exe"
poetry env info
```

※コマンドプロンプトの場合

```
poetry env use "%HOMEPATH%\.pyenv\pyenv-win\versions\3.10.5\python.exe"
poetry env info
```
