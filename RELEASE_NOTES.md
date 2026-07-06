## v0.2.0

### Added

- 両面印刷に対応しました。
  - `--duplex`: 長辺とじの両面印刷
  - `--duplex long`: 長辺とじの両面印刷を明示
  - `--duplex short`: 短辺とじの両面印刷
  - `--simplex`: 片面印刷を明示

### Changed

- PDFをPostScriptへ変換した後、必要に応じてPostScript内へ印刷設定を挿入するようにしました。
- 両面印刷の指定には、PostScriptの `setpagedevice` を利用します。

### Known Issues

- 白黒印刷は未対応です。
  - Windows側では `PageOutputColor = Monochrome` の指定が確認できています。
  - macOSからの直接IPP/PostScript送信で同等の指定を安定して反映する方式は未確定です。
- 部数指定は未対応です。
- GUIは未対応です。

### Notes

このリリースは、GUI作成前にCLI側の印刷オプションを整理するための更新です。