# CCF (Claude Code Force) インストール手順

## 概要
CCF は Claude Code の完全自動化システムです。複数のセッションを安全に管理し、プロジェクトごとの設定を自動化します。

## インストール手順

### 1. スクリプトファイルの配置
```bash
# .claude ディレクトリを作成
mkdir -p ~/.claude

# ccf スクリプトをダウンロード/コピー
cp claude-complete.py ~/.claude/
```

### 2. 実行権限の設定
```bash
chmod +x ~/.claude/claude-complete.py
```

### 3. エイリアスの設定
以下を `~/.bashrc` または `~/.zshrc` に追加：

```bash
# Claude Code 自動化システム設定
export CLAUDE_LOGIN_SCRIPT="$HOME/claude-login.py"
export CLAUDE_VENV_PATH="$HOME/venv"

# CCF エイリアス
alias ccf='python3 ~/.claude/claude-complete.py'
alias claude-complete='python3 ~/.claude/claude-complete.py'
```

### 4. 設定の確認
```bash
# 設定テンプレートを表示
ccf --setup

# 設定を反映
source ~/.bashrc  # または source ~/.zshrc
```

## 環境変数の設定

### 必須環境変数
- `CLAUDE_LOGIN_SCRIPT`: 自動ログインスクリプトのパス
- `CLAUDE_VENV_PATH`: Python仮想環境のパス

### 設定例
```bash
# Linux/macOS
export CLAUDE_LOGIN_SCRIPT="$HOME/claude-login.py"
export CLAUDE_VENV_PATH="$HOME/venv"

# Windows WSL
export CLAUDE_LOGIN_SCRIPT="/mnt/c/Users/username/claude-login.py"
export CLAUDE_VENV_PATH="/mnt/c/Users/username/venv"
```

## 使用方法

### 基本的な使用
```bash
# デフォルト（他のセッションを保護）
ccf

# プロジェクトタイプを指定
ccf web-dev
ccf data-science
ccf game-dev
ccf mobile-dev
```

### オプション
```bash
# 他のセッションを強制終了
ccf --no-parallel

# クリーンアップをスキップ
ccf --no-cleanup

# 初期設定を表示
ccf --setup
```

## トラブルシューティング

### 仮想環境が見つからない
```bash
# 環境変数を確認
echo $CLAUDE_VENV_PATH

# パスを修正
export CLAUDE_VENV_PATH="/path/to/your/venv"
```

### ログインスクリプトが見つからない
```bash
# 環境変数を確認
echo $CLAUDE_LOGIN_SCRIPT

# パスを修正
export CLAUDE_LOGIN_SCRIPT="/path/to/your/claude-login.py"
```

### 権限エラー
```bash
# 実行権限を確認
chmod +x ~/.claude/claude-complete.py
```

## 他のPCへの移行

1. `claude-complete.py` を新しいPCにコピー
2. 環境変数を新しい環境に合わせて設定
3. `ccf --setup` で設定を確認
4. エイリアスを設定

これで他のPCでも同じように使用できます。