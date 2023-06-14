# WebUI Generation Config Prompt

これは AUTOMATIC1111 氏の [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 用の拡張です。

画像生成時の横幅やステップ数, CFGScaleなどの設定をプロンプトで設定することが出来ます。

## インストール

`stable-diffusion-webui` の `Install from URL` からこのリポジトリのURL `https://github.com/Taremin/webui-generation-config-prompt` を入力してインストールしてください。

## 機能

- 解像度のWidth, Heightを入れ替える
- その他, `StableDiffusionProcessing` クラスのすべてのプロパティを設定する機能
    - `width`, `height`, `steps`, `cfg_scale`, `sampler_name` などの主要なもの以外はまともに動作しない可能性があります

## 使用例

### swap

解像度の縦横を入れ替えます。

```
<config:swap>
1girl
```

### set

画像生成の設定を直接書き換えます。
複数を同時に指定可能です。
下記の例では縦横の解像度が128x128の画像を10stepで生成します。
（もちろん、stepsも上の行で同時に設定しても良いです）

```
<config:set:width=128:height=128>
<config:set:steps=10>
1girl
```

## 設定項目

### Trigger Word

`GenarationConfigPrompt` を有効にする語句の変更が出来ます。
デフォルトでは `config` となっていますが別のものに変更することが可能です。

## ライセンス

[MIT](./LICENSE)
