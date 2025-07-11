#!/bin/bash

# CCF (Claude Code Force) ワンライナーインストールスクリプト
# Usage: curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/ccf/main/install.sh | bash

set -e

# 色付きメッセージ用の関数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# CCF インストール開始
print_info "🎯 CCF (Claude Code Force) インストール開始"

# 必須コマンドの確認
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 が見つかりません。Python 3.6+ をインストールしてください。"
    exit 1
fi

if ! command -v claude &> /dev/null; then
    print_error "Claude Code CLI が見つかりません。先にClaude Code CLIをインストールしてください。"
    exit 1
fi

print_success "✅ 必須コマンドが確認されました"

# .claude ディレクトリの作成
print_info "📂 .claude ディレクトリを作成中..."
mkdir -p ~/.claude

# メインスクリプトのダウンロード
print_info "⬇️  メインスクリプトをダウンロード中..."
if command -v curl &> /dev/null; then
    curl -fsSL https://raw.githubusercontent.com/muumuu8181/ccf/main/claude-complete.py -o ~/.claude/claude-complete.py
elif command -v wget &> /dev/null; then
    wget -q https://raw.githubusercontent.com/muumuu8181/ccf/main/claude-complete.py -O ~/.claude/claude-complete.py
else
    print_error "curl または wget が必要です。"
    exit 1
fi

# 実行権限の設定
print_info "🔧 実行権限を設定中..."
chmod +x ~/.claude/claude-complete.py

# base-CLAUDE.mdのダウンロード
print_info "📋 CCF設定ファイルをダウンロード中..."
if command -v curl &> /dev/null; then
    curl -fsSL https://raw.githubusercontent.com/muumuu8181/ccf/main/base-CLAUDE.md -o ~/.claude/base-CLAUDE.md
elif command -v wget &> /dev/null; then
    wget -q https://raw.githubusercontent.com/muumuu8181/ccf/main/base-CLAUDE.md -O ~/.claude/base-CLAUDE.md
fi

# シェル検出とエイリアス設定
print_info "⚙️  エイリアスを設定中..."
SHELL_RC=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    print_warning "シェルが自動検出できませんでした。手動で設定してください。"
fi

if [[ -n "$SHELL_RC" ]]; then
    # エイリアスが既に存在するかチェック
    if ! grep -q "alias ccf=" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# CCF (Claude Code Force) エイリアス" >> "$SHELL_RC"
        echo 'alias ccf="python3 ~/.claude/claude-complete.py"' >> "$SHELL_RC"
        echo 'alias claude-complete="python3 ~/.claude/claude-complete.py"' >> "$SHELL_RC"
        print_success "✅ エイリアスが $SHELL_RC に追加されました"
    else
        print_info "ℹ️  エイリアスは既に設定されています"
    fi
fi

# 環境変数の設定案内
print_info "🔧 環境変数を設定してください:"
echo ""
echo "# 以下を $SHELL_RC に追加:"
echo 'export CLAUDE_LOGIN_SCRIPT="$HOME/claude-login.py"'
echo 'export CLAUDE_VENV_PATH="$HOME/venv"'
echo ""

# インストール完了
print_success "🎉 CCF インストール完了!"
echo ""
print_info "次のステップ:"
echo "1. 新しいターミナルを開くか、'source $SHELL_RC' を実行"
echo "2. 環境変数を設定: 'ccf --setup' で詳細確認"
echo "3. ccf を実行: 'ccf'"
echo ""
print_info "詳細な使用方法: https://github.com/muumuu8181/ccf"

# 設定確認の提案
echo ""
read -p "今すぐ設定を確認しますか? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 ~/.claude/claude-complete.py --setup
fi