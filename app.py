# ==============================================================================
# デスクトップ OCR 検索ツール (NDLOCR-Lite 統合版)
# Copyright (c) 2026 3knek0
#
# 【環境構築手順】
# 1. リポジトリのクローン:
#    git clone https://github.com/ndl-lab/ndlocr-lite
#
# 2. 依存ライブラリのインストール:
#    pip install opencv-python mss numpy tkinter pyyaml omegaconf tqdm
#    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
#    pip install onnxruntime
#
#    ※ もし requirements.txt から一括導入する場合はバージョン競合に注意:
#    pip install -r ndlocr-lite/requirements.txt
#    (onnxruntime のエラーが出る場合は、個別に pip install onnxruntime を実行)
#
# 3. 実行構成:
#    - 本スクリプトと同じ階層に "ndlocr-lite" フォルダが存在すること。
#    - ndlocr-lite/src/model/ 内に .onnx モデルファイルが存在すること。
# ==============================================================================
import sys
import os
import cv2
import mss
import numpy as np
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

# --- NDLOCR-Liteをロードするための設定 ---
current_dir = Path(__file__).parent.absolute()
ndl_src_path = current_dir / "ndlocr-lite" / "src"
if str(ndl_src_path) not in sys.path:
    sys.path.append(str(ndl_src_path))

# ocr.py モジュールをインポート
try:
    import ocr
    print("NDLOCR-Lite モジュールの読み込みに成功しました。")
except ImportError as e:
    print(f"インポートエラー: {e}")
    sys.exit(1)

# --- OCRエンジンを管理するブリッジクラス ---
class NDLOCRBridge:
    def __init__(self):
        # ocr.pyの関数が期待する引数オブジェクトを模倣
        class Args:
            def __init__(self):
                base = Path(ocr.__file__).parent
                self.device = "cpu"  # GPUを使うなら "cuda"
                self.det_weights = str(base / "model" / "deim-s-1024x1024.onnx")
                self.det_classes = str(base / "config" / "ndl.yaml")
                self.det_score_threshold = 0.2
                self.det_conf_threshold = 0.25
                self.det_iou_threshold = 0.2
                self.rec_weights = str(base / "model" / "parseq-ndl-16x768-100-tiny-165epoch-tegaki2.onnx")
                self.rec_weights30 = str(base / "model" / "parseq-ndl-16x256-30-tiny-192epoch-tegaki3.onnx")
                self.rec_weights50 = str(base / "model" / "parseq-ndl-16x384-50-tiny-146epoch-tegaki2.onnx")
                self.rec_classes = str(base / "config" / "NDLmoji.yaml")
        
        self.args = Args()
        print("モデルをロード中... (初回のみ時間がかかります)")
        # 各種モデルの初期化
        self.detector = ocr.get_detector(self.args)
        self.recognizer100 = ocr.get_recognizer(self.args)
        self.recognizer30 = ocr.get_recognizer(self.args, weights_path=self.args.rec_weights30)
        self.recognizer50 = ocr.get_recognizer(self.args, weights_path=self.args.rec_weights50)
        print("モデルのロードが完了しました！")

    def execute_ocr(self, img):
        """画像(BGR)を受け取り、認識結果をリストで返す"""
        # 1. 文字領域の検出
        detections, _ = ocr.process_detector(self.detector, "capture", img, "output", issaveimg=False)
        
        all_line_objs = []
        results = []
        
        # 2. 検出結果を認識用オブジェクト(RecogLine)に変換
        for idx, det in enumerate(detections):
            xmin, ymin, xmax, ymax = map(int, det["box"])
            # 範囲外チェックをして切り出し
            line_img = img[max(0, ymin):ymax, max(0, xmin):xmax, :]
            if line_img.size == 0: continue
            
            line_obj = ocr.RecogLine(line_img, idx, 100.0)
            all_line_objs.append(line_obj)
            results.append({"text": "", "box": [xmin, ymin, xmax, ymax]})

        if not all_line_objs:
            return []

        # 3. 文字認識の実行 (カスケード方式)
        pred_texts = ocr.process_cascade(
            all_line_objs, self.recognizer30, self.recognizer50, self.recognizer100, is_cascade=True
        )

        # 4. テキストを結果リストに格納
        for i, text in enumerate(pred_texts):
            if i < len(results):
                results[i]["text"] = text
                
        return results

# --- 初期化 ---
bridge = None
sct = mss.mss()
is_running = True
is_search_window_open = False

def capture_screen():
    monitor = sct.monitors[1] 
    img = np.array(sct.grab(monitor))
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def close_search_window():
    global is_search_window_open
    try:
        cv2.destroyWindow("Search Result")
    except:
        pass
    is_search_window_open = False

def run_search(event=None):
    global is_search_window_open, bridge
    
    # 初回実行時にエンジンを初期化
    if bridge is None:
        try:
            bridge = NDLOCRBridge()
        except Exception as e:
            messagebox.showerror("Error", f"エンジンの初期化に失敗しました:\n{e}")
            return

    target_text = entry.get().strip()
    if not target_text:
        return

    root.title(f"検索中: \"{target_text}\"")
    root.update()

    print(f"Searching for: {target_text}...")
    screen = capture_screen()
    
    try:
        # OCR実行
        ocr_results = bridge.execute_ocr(screen)
        found = False
        
        for res in ocr_results:
            if target_text in res['text']:
                box = res['box']
                cv2.rectangle(screen, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 3)
                found = True
        
        if found:
            print("見つかりました。")
            root.title(f"発見: \"{target_text}\"")
            window_name = "Search Result"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.imshow(window_name, screen)
            is_search_window_open = True
            root.after(5000, close_search_window)
        else:
            print("見つかりませんでした。")
            root.title("見つかりませんでした")
            messagebox.showinfo("OCR結果", f"「{target_text}」は見つかりませんでした。")
            
    except Exception as e:
        print(f"OCR実行エラー: {e}")
        root.title("OCRエラー発生")

def process_cv_events():
    if is_running:
        if is_search_window_open:
            cv2.waitKey(1)
        root.after(100, process_cv_events)

def on_closing():
    global is_running
    is_running = False
    cv2.destroyAllWindows()
    root.destroy()
    sct.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("NDL-OCR Search Tool")
    root.geometry("400x120")
    root.attributes("-topmost", True)

    lbl = tk.Label(root, text="画面内を検索する文字:")
    lbl.pack(pady=5)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)
    entry.bind('<Return>', run_search)
    entry.focus_set()

    btn = tk.Button(root, text="検索実行", command=run_search)
    btn.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    process_cv_events()
    root.mainloop()
