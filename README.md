# Desktop OCR Search Tool (NDLOCR-Lite 統合版)

画面内に表示されている文字をAI（OCR）で解析し、指定したキーワードがどこにあるかを瞬時に探し出すデスクトップ検索ツールです。国立国会図書館（NDL）が公開している `ndlocr-lite` をエンジンとして利用しています。

## 🌟 特徴
- **リアルタイム検索**: デスクトップ全体をキャプチャし、入力した文字列をOCRで探します。
- **視覚的なフィードバック**: 見つかった場所を赤い枠で強調表示します。
- **軽量動作**: ONNXランタイムを利用し、CPU環境でも動作可能です。

## 📸 デモ (動作イメージ)
1. アプリを起動すると入力ダイアログが表示されます。
2. 検索したい文字を入力して Enter を押します。
3. 画面内で一致した箇所が数秒間ハイライトされます。

## 🛠 セットアップ

### 1. 外部エンジンのクローン
本ツールと同じディレクトリで、NDL公式のリポジトリをクローンしてください。
```bash
git clone [https://github.com/ndl-lab/ndlocr-lite](https://github.com/ndl-lab/ndlocr-lite)

### 2.必要なライブラリのインストール
pip install opencv-python mss numpy tkinter pyyaml omegaconf tqdm onnxruntime
pip install torch torchvision --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)

### 3.モデルファイルの配置
ndlocr-lite/src/model/ 内に必要な .onnx モデルファイルが配置されていることを確認してください。

### 4.使い方
python app.py

