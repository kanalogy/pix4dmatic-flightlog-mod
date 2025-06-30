# pix4dmatic-flightlog-mod

**以下は、とりあえず処理できる、といった程度の仮の設定。**
**実用上は、検証点との比較などを行い、設定を詰める必要がある。**

通常のMJpegの処理に加えて、以下の処理が必要になる。
# MJpegでの処理設定
出力タブ --> フライトデータ --> 出力座標系「WGS84」、高さにJPGEO2024の標高を使うを「オフ」
外部プログラムタブ --> exiftoolを使用 --> カメラメーカーとカメラモデルを指定
※GoProと一部スマホ以外はMJpegで設定できないため、後から自分で書き込む必要がある。
# flightlog.txtの改変
Pix4Dmaticでflihgtlogを読み込むためのフォーマットに変更する
変更の概要は以下の通り。

`LongitudeAccuracy, LatitudeAccuracy`を、`Horizontal accuracy`などとしてひとつにする。
	- MJpegでは水平精度はXYで同じため、どちらかを破棄すれば良い。

Pitchの値を(X)としたとき、f(x) = 90 - (x) になるようにPitchの値を書き換える。
- MJpegで出力される値とPIX4Dmaticで扱うPitch角の基準が異なるため
	- MJpegは、真下が+90°、水平が0°、真上が-90°
	- PIX4Dmaticは、真下が0°、水平が+90°、真上が+180°

上記で改変した値を含め、以下のように並べ替える。
- `Name, Latitude, Longitude, Altitude, Yaw, Pitch, Roll, Horizontal accuracy, AltitudeAccuracy`

# PIX4Dmaticでの処理手順
画像をインポート
ファイル --> インポート --> 画像の位置と向き、から上記で改変したflightlog.txtを指定して読み込む。
水平座標系は「WGS84」、鉛直座標系は「」とする。
## キャリブレーション
**テンプレート**
- 「PIX4Dcatch」または「3Dモデル」などを選択
**パイプライン**
- 「信頼性の高い位置と向き情報」「スケーラブル標準」などを選択
	- それぞれ、flightlog.txtの値の重み付けが異なる
**カメラ内部パラメータ**
- 撮影機材に準じた値にする。
- 実際と乖離しすぎるとキャリブレーション不良の原因となる。
