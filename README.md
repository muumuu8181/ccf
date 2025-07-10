# CCF - Claude Code Force

Claude Codeの完全自動化システム。複数セッションの安全な管理とプロジェクト自動化を提供します。

## 特徴

- 🛡️ **セーフモード**: 他のClaude Codeセッションを保護（デフォルト）
- 🚀 **自動ログイン**: 認証の自動化
- 📋 **プロジェクト自動検出**: 自動的にプロジェクトタイプを判定
- ⚙️ **設定自動化**: CLAUDE.mdの自動生成
- 🔄 **継続実行**: セッション終了時の自動再起動

## クイックスタート

### ワンライナーインストール
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/ccf/main/install.sh | bash
```

### 手動インストール
```bash
# ディレクトリ作成
mkdir -p ~/.claude

# スクリプトダウンロード
curl -o ~/.claude/claude-complete.py https://raw.githubusercontent.com/YOUR_USERNAME/ccf/main/claude-complete.py

# 実行権限設定
chmod +x ~/.claude/claude-complete.py

# エイリアス設定
echo 'alias ccf="python3 ~/.claude/claude-complete.py"' >> ~/.bashrc
source ~/.bashrc
```

## 環境設定

```bash
# 必須環境変数
export CLAUDE_LOGIN_SCRIPT="$HOME/claude-login.py"
export CLAUDE_VENV_PATH="$HOME/venv"

# 設定確認
ccf --setup
```

## 使用方法

### 基本使用
```bash
# デフォルト（他セッション保護）
ccf

# プロジェクトタイプ指定
ccf web-dev
ccf data-science
ccf game-dev
```

### オプション
```bash
# 他セッション強制終了
ccf --no-parallel

# クリーンアップスキップ
ccf --no-cleanup

# 設定表示
ccf --setup
```

## 対応プロジェクトタイプ

- `web-dev`: Web開発（React, Vue, Angular等）
- `data-science`: データサイエンス（Python, Jupyter等）
- `game-dev`: ゲーム開発（Unity等）
- `mobile-dev`: モバイル開発（React Native, Flutter等）
- `general`: 汎用開発

## 要件

- Python 3.6+
- Claude Code CLI
- 仮想環境（推奨）

## ライセンス

MIT License

## 貢献

Issue や Pull Request をお待ちしています。

## トラブルシューティング

詳細は [インストール手順](INSTALL.md) を参照してください。