# Desktop OCR Search Tool (NDLOCR-Lite 統合版)

画面内に表示されている文字をAI（OCR）で解析し、指定したキーワードがどこにあるかを瞬時に探し出すデスクトップ検索ツールです。国立国会図書館（NDL）が公開している `ndlocr-lite` をエンジンとして利用しています。

## 🌟 特徴
- **リアルタイム検索**: デスクトップ全体をキャプチャし、入力した文字列をOCRで探します。
- **視覚的なフィードバック**: 見つかった場所を赤い枠で強調表示し、数秒後に自動で消えます。
- **軽量動作**: ONNXランタイムを利用し、CPU環境でも動作可能です。

## 🛠 環境構築手順

### 1. リポジトリのクローン
本ツールと同じ階層に `ndlocr-lite` フォルダが存在するようにクローンしてください。
```bash
git clone https://github.com/ndl-lab/ndlocr-lite
```

### ２．依存ライブラリのインストール
以下のコマンドを実行して、必要なライブラリを導入してください。

```
pip install opencv-python mss numpy tkinter pyyaml omegaconf tqdm onnxruntime
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

※requirements.txt から一括導入する場合はバージョン競合に注意してください。
　onnxruntime のエラーが出る場合は、個別に pip install onnxruntime を実行してください。

### ３．モデルファイルの配置
ndlocr-lite/src/model/ 内に、以下の .onnx モデルファイルが存在することを確認してください。

```
deim-s-1024x1024.onnx
parseq-ndl-16x768-100-tiny-165epoch-tegaki2.onnx
parseq-ndl-16x256-30-tiny-192epoch-tegaki3.onnx
parseq-ndl-16x384-50-tiny-146epoch-tegaki2.onnx
```

## 🚀 使い方
```bash
python app.py
```

## 📜 ライセンス
このプロジェクトは MITライセンス の下で公開されています。
詳細は LICENSE ファイルをご覧ください。
