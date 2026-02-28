# Desktop OCR Search Tool (NDLOCR-Lite 統合版)

画面内に表示されている文字をAI（OCR）で解析し、指定したキーワードがどこにあるかを瞬時に探し出すデスクトップ検索ツールです。国立国会図書館（NDL）が公開している `ndlocr-lite` をエンジンとして利用しています。

## 🌟 特徴
- **リアルタイム検索**: デスクトップ全体をキャプチャし、入力した文字列をOCRで探します。
- **視覚的なフィードバック**: 見つかった場所を赤い枠で強調表示します。
- **軽量動作**: ONNXランタイムを利用し、CPU環境でも動作可能です。

## 📸 動作イメージ
1. アプリを起動すると、デスクトップの最前面に入力ダイアログが表示されます。
2. 検索したい文字を入力して Enter を押すと、画面全体のOCR解析が始まります。
3. 文字が見つかった場合、その場所が赤い枠で数秒間ハイライトされます。

## 🛠 セットアップ

### 1. 外部エンジンのクローン
本ツールと同じディレクトリで、NDL公式のリポジトリをクローンしてください。
```bash
git clone https://github.com/ndl-lab/ndlocr-lite

### 2. 必要なライブラリのインストール
以下のコマンドを実行して、必要な依存ライブラリをインストールしてください。
```bash
# 基本ライブラリ
pip install opencv-python mss numpy pyyaml omegaconf tqdm onnxruntime

# PyTorch (CPU版)
pip install torch torchvision --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)

