## v0.3.0

### Added

- `--mono` / `-m` オプションを追加
  - PDFをグレースケールPostScriptへ変換してから送信できます
  - Ghostscriptを使用します
- 白黒印刷に関する既知制限をREADMEに追加

### Changed

- READMEの使用方法とオプション説明を更新
- 白黒印刷の扱いを「対応済み」ではなく「グレースケール変換送信」として明確化

### Known limitations

- `--mono` はプリンター側の白黒ジョブ判定や白黒課金を保証しません
- 現在の学内プリンター環境では、グレースケール化したジョブもカラーとして認識されます
- Windows公式ドライバーではRicoh RPCS形式のジョブが送信されており、白黒判定もRPCSデータに依存している可能性があります
- macOS上で完結する現在の実装では、白黒課金・白黒ジョブ化は未対応です

### Notes

このリリースでは、白黒印刷対応に向けた検証として以下を確認しました。

- IPP属性 `print-color-mode=monochrome`
- PJL `DATAMODE=GRAYSCALE`
- PostScript / Ghostscriptによるグレースケール変換
- PDF直接送信
- PCL XL monochrome送信

これらの方式では、プリンター側で白黒ジョブとして認識されませんでした。  
そのため、v0.3.0では白黒印刷対応ではなく、実験的なグレースケール変換送信機能として提供します。