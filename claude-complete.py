#!/usr/bin/env python3

import subprocess
import time
import os
import sys
import argparse
from pathlib import Path

class ClaudeCompleteSystem:
    def __init__(self):
        self.claude_dir = Path.home() / ".claude"
        self.work_dir = Path.cwd()
        # 環境変数または設定ファイルから取得、デフォルト値を設定
        self.claude_login_script = os.getenv('CLAUDE_LOGIN_SCRIPT', str(Path.home() / "claude-login.py"))
        self.venv_path = os.getenv('CLAUDE_VENV_PATH', str(Path.home() / "venv"))
        self.log_file = Path.home() / ".claude" / "ccf_session_log.txt"
        
    def log_action(self, action):
        """全ての動作をログに記録"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {action}\n")
        
    def cleanup_processes(self, parallel_mode=True, skip_cleanup=False):
        """既存のClaude関連プロセスをクリーンアップ（--no-cleanupオプションでスキップ可能）"""
        if skip_cleanup:
            self.log_action("ccf開始 - クリーンアップスキップモード: 他のセッションを保護")
            print("🛡️  クリーンアップスキップ: 他のClaude Codeセッションを保護します")
            print("✅ 他のセッションを保護しました")
            print("🔄 処理を続行します...")
            time.sleep(1)
            return
            
        if parallel_mode:
            self.log_action("ccf開始 - 並列モード: 現在のセッションのみ保護")
            print("🧹 並列モード: 現在のセッションを保護してクリーンアップ中...")
        else:
            self.log_action("ccf開始 - 通常モード: 全プロセスクリーンアップ")
            print("🧹 通常モード: 既存プロセスをクリーンアップ中...")
        
        try:
            # 現在のプロセスツリーを取得して除外
            current_pid = os.getpid()
            parent_pid = os.getppid()
            
            # 現在のプロセスツリーに含まれるPIDを収集
            exclude_pids = {current_pid, parent_pid}
            
            # 現在のプロセスの子プロセスも除外対象に追加
            try:
                children_result = subprocess.run(['pgrep', '-P', str(current_pid)], 
                                               capture_output=True, text=True)
                if children_result.returncode == 0:
                    child_pids = children_result.stdout.strip().split('\n')
                    exclude_pids.update(int(pid) for pid in child_pids if pid.isdigit())
            except:
                pass
            
            # 並列モードの場合は、他のccfプロセスも除外
            if parallel_mode:
                try:
                    ccf_processes = subprocess.run(['pgrep', '-f', 'claude-complete'], 
                                                 capture_output=True, text=True)
                    if ccf_processes.returncode == 0:
                        ccf_pids = ccf_processes.stdout.strip().split('\n')
                        exclude_pids.update(int(pid) for pid in ccf_pids if pid.isdigit())
                except:
                    pass
            
            # Claude関連プロセスを検索
            claude_processes = subprocess.run(['pgrep', '-f', 'claude'], 
                                            capture_output=True, text=True)
            
            if claude_processes.returncode == 0:
                claude_pids = claude_processes.stdout.strip().split('\n')
                for pid_str in claude_pids:
                    if pid_str.isdigit():
                        pid = int(pid_str)
                        if pid not in exclude_pids:
                            try:
                                subprocess.run(['kill', str(pid)], capture_output=True)
                                print(f"🔄 プロセス {pid} を終了")
                            except:
                                pass
            
            # ポート54545のプロセスも同様に処理（並列モードでは慎重に）
            if not parallel_mode:
                port_processes = subprocess.run(['lsof', '-t', '-i:54545'], 
                                              capture_output=True, text=True)
                if port_processes.returncode == 0:
                    port_pids = port_processes.stdout.strip().split('\n')
                    for pid_str in port_pids:
                        if pid_str.isdigit():
                            pid = int(pid_str)
                            if pid not in exclude_pids:
                                try:
                                    subprocess.run(['kill', str(pid)], capture_output=True)
                                    print(f"🔄 ポート54545使用プロセス {pid} を終了")
                                except:
                                    pass
            
            if parallel_mode:
                print("✅ 並列モード: 現在のセッションを保護しました")
            else:
                print("✅ プロセス終了完了（現在のセッションは保護されました）")
            print("🔄 処理を続行します...")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ プロセス終了処理でエラー: {e}")
            print("🔄 処理を続行します...")
    
    def check_authentication(self):
        """認証状態をチェック"""
        self.log_action("認証状態チェック開始")
        print("🔐 認証状態をチェック中...")
        try:
            result = subprocess.run(['claude', 'config', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ 認証済み")
                return True
            else:
                print("❌ 認証が必要")
                return False
        except subprocess.TimeoutExpired:
            print("❌ 認証タイムアウト - ログインが必要")
            return False
        except Exception as e:
            print(f"❌ 認証確認エラー: {e}")
            return False
    
    def run_auto_login(self):
        """自動ログインスクリプトを実行"""
        self.log_action("自動ログイン開始 - GUI操作開始")
        print("🚀 自動ログインを実行中...")
        
        # 仮想環境の確認
        if not os.path.exists(self.venv_path):
            print("❌ 仮想環境が見つかりません")
            print(f"💡 環境変数 CLAUDE_VENV_PATH で仮想環境パスを設定してください（現在: {self.venv_path}）")
            return False
            
        # ログインスクリプトの確認
        if not os.path.exists(self.claude_login_script):
            print("❌ ログインスクリプトが見つかりません")
            print(f"💡 環境変数 CLAUDE_LOGIN_SCRIPT でスクリプトパスを設定してください（現在: {self.claude_login_script}）")
            return False
            
        try:
            # スクリプトのディレクトリに移動して実行
            script_dir = Path(self.claude_login_script).parent
            script_name = Path(self.claude_login_script).name
            cmd = f'cd {script_dir} && source {self.venv_path}/bin/activate && python {script_name}'
            print("🔄 ログインスクリプト実行中（GUI操作が開始されます）...")
            
            # バックグラウンドで実行
            process = subprocess.Popen(['bash', '-c', cmd])
            
            # ログイン完了まで待機（最大60秒）
            print("⏳ ログイン完了を待機中...")
            for i in range(60):
                if self.check_authentication():
                    print("✅ ログイン完了")
                    return True
                time.sleep(1)
                if i % 10 == 0:
                    print(f"⏳ 待機中... ({i}/60秒)")
            
            print("❌ ログインタイムアウト")
            return False
            
        except Exception as e:
            print(f"❌ ログインエラー: {e}")
            return False
    
    def detect_project_type(self):
        """プロジェクトタイプを自動検出"""
        print("🔍 プロジェクトタイプを自動検出中...")
        
        # ファイル拡張子と内容でプロジェクトタイプを判定
        if (self.work_dir / "package.json").exists() or (self.work_dir / "tsconfig.json").exists():
            if (self.work_dir / "package.json").exists():
                with open(self.work_dir / "package.json", 'r') as f:
                    content = f.read()
                    if any(tech in content for tech in ["react", "vue", "angular", "next", "nuxt"]):
                        return "web-dev"
            return "web-dev"
        elif (self.work_dir / "requirements.txt").exists() or (self.work_dir / "setup.py").exists():
            if (self.work_dir / "requirements.txt").exists():
                with open(self.work_dir / "requirements.txt", 'r') as f:
                    content = f.read()
                    if any(tech in content for tech in ["pandas", "numpy", "matplotlib", "jupyter", "scikit-learn"]):
                        return "data-science"
            return "data-science"
        elif any(self.work_dir.glob("*.unity")) or (self.work_dir / "Assets").exists():
            return "game-dev"
        elif (self.work_dir / "android").exists() or (self.work_dir / "ios").exists():
            return "mobile-dev"
        else:
            return "general"
    
    def setup_claude_md(self, project_type, force_setup=False):
        """CLAUDE.mdの自動設定（--force-setupオプションで強制上書き可能）"""
        print("📋 CLAUDE.mdを設定中...")
        
        claude_md_path = self.work_dir / "CLAUDE.md"
        if not claude_md_path.exists() or force_setup:
            if force_setup and claude_md_path.exists():
                print("⚠️  強制モード: 既存のCLAUDE.mdを上書きします")
            
            # 基本設定をコピー
            base_md = self.claude_dir / "base-CLAUDE.md"
            if base_md.exists():
                with open(base_md, 'r') as src, open(claude_md_path, 'w') as dst:
                    dst.write(src.read())
                print(f"✅ base-CLAUDE.mdからコピーしました")
            else:
                print("⚠️  base-CLAUDE.mdが見つかりません。基本的なCLAUDE.mdを作成します。")
                with open(claude_md_path, 'w') as dst:
                    dst.write("# Claude Code 基本設定\n\n## 🎯 起動時の特別ルール\n**重要**: セッション開始時には必ず最初に \"Hello! CCF (Claude Code Force) 起動しました！🚀 今日も効率的に作業を進めましょう！\" と挨拶する\n\n## 🚀 基本動作方針\n- **許可を求めずに実行**: 可能な限り自分で判断して全て進める\n")
            
            # プロジェクト固有情報を追加
            with open(claude_md_path, 'a') as f:
                f.write(f"""

## プロジェクト情報
- **ディレクトリ**: {self.work_dir}
- **プロジェクトタイプ**: {project_type}
- **検出日時**: {time.strftime('%Y-%m-%d %H:%M:%S')}

## 検出されたファイル
""")
                # 主要ファイルを自動検出
                for file in ["package.json", "requirements.txt", "setup.py", "tsconfig.json"]:
                    if (self.work_dir / file).exists():
                        f.write(f"- {file}\n")
            
            print("✅ CLAUDE.mdを作成しました")
        else:
            print("✅ 既存のCLAUDE.mdを使用します（--force-setupで強制更新可能）")
    
    def apply_project_settings(self, project_type):
        """プロジェクト設定を適用"""
        print("⚙️ プロジェクト設定を適用中...")
        
        # claude-setupスクリプトを実行
        setup_script = self.claude_dir / "claude-setup.sh"
        if setup_script.exists():
            try:
                subprocess.run([str(setup_script), project_type], 
                             capture_output=True, timeout=30)
                print(f"✅ {project_type}設定を適用しました")
            except Exception as e:
                print(f"⚠️ 設定適用エラー: {e}")
    
    def launch_claude(self, additional_args):
        """Claude Codeを起動"""
        self.log_action(f"Claude Code起動開始 - 引数: {additional_args}")
        print("🚀 Claude Codeを起動中...")
        
        # 環境変数を設定
        env = os.environ.copy()
        env.update({
            'CLAUDE_AUTO_MODE': 'true',
            'CLAUDE_PROJECT_TYPE': getattr(self, 'project_type', 'general'),
            'CLAUDE_WORK_DIR': str(self.work_dir)
        })
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🎯 Claude Code 完全自動化システム起動完了")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("")
        
        # Claude Codeを起動（継続ループ）
        while True:
            try:
                cmd = ['claude'] + additional_args
                self.log_action(f"Claude Code実行中: {' '.join(cmd)}")
                result = subprocess.run(cmd, env=env)
                self.log_action(f"Claude Code終了 - 終了コード: {result.returncode}")
                
                # 正常終了時の継続確認
                print("\n" + "="*50)
                choice = input("Claude Codeを再起動しますか？ (y/n): ").strip().lower()
                if choice != 'y':
                    self.log_action("ユーザーがccfコマンド終了を選択")
                    print("👋 ccfコマンド終了")
                    break
                else:
                    self.log_action("ユーザーがClaude Code再起動を選択")
                    
            except KeyboardInterrupt:
                self.log_action("Ctrl+Cでccf強制終了")
                print("\n👋 Claude Code終了")
                break
            except Exception as e:
                print(f"❌ Claude Code起動エラー: {e}")
                choice = input("再試行しますか？ (y/n): ").strip().lower()
                if choice != 'y':
                    break
    
    def run(self, project_type=None, additional_args=None, parallel_mode=True, skip_cleanup=False, force_setup=False):
        """メイン実行関数"""
        if additional_args is None:
            additional_args = []
            
        self.skip_cleanup = skip_cleanup
        self.force_setup = force_setup
        self.log_action(f"ccfコマンド開始 - 作業ディレクトリ: {self.work_dir}, 並列モード: {parallel_mode}, クリーンアップスキップ: {skip_cleanup}, 強制セットアップ: {force_setup}")
        print("🎯 Claude Code 完全自動化システム")
        print(f"作業ディレクトリ: {self.work_dir}")
        if skip_cleanup:
            print("🛡️  セーフモード: 他のClaude Codeセッションを保護")
        elif parallel_mode:
            print("🔄 並列実行モード: 他のClaude Codeセッションを保護")
        else:
            print("🔄 通常モード: 他のClaude Codeセッションを終了")
        
        if force_setup:
            print("⚡ 強制セットアップモード: CLAUDE.mdを強制更新")
        print("")
        
        # 1. プロセスクリーンアップ
        self.cleanup_processes(parallel_mode, skip_cleanup=getattr(self, 'skip_cleanup', False))
        
        # 2. 認証確認
        if not self.check_authentication():
            print("🔐 認証が必要です。自動ログインを開始...")
            if not self.run_auto_login():
                print("❌ 自動ログインに失敗しました")
                print("💡 手動でログインしてください:")
                print("   1. 新しいターミナルで 'claude' を実行")
                print("   2. ブラウザでログイン")
                print("   3. 再度このスクリプトを実行")
                return False
        
        # 3. プロジェクトタイプの決定
        if project_type is None:
            project_type = self.detect_project_type()
            print(f"📋 検出されたプロジェクトタイプ: {project_type}")
        else:
            print(f"📋 指定されたプロジェクトタイプ: {project_type}")
        
        self.project_type = project_type
        
        # 4. 設定の準備
        self.setup_claude_md(project_type, force_setup=getattr(self, 'force_setup', False))
        self.apply_project_settings(project_type)
        
        # 5. Claude Code起動
        self.launch_claude(additional_args)
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Claude Code 完全自動化システム')
    parser.add_argument('project_type', nargs='?', 
                       choices=['game-dev', 'data-science', 'web-dev', 'mobile-dev', 'general'],
                       help='プロジェクトタイプ（自動検出も可能）')
    parser.add_argument('--no-parallel', action='store_true',
                       help='通常モード: 他のClaude Codeセッションを終了してから新しいセッションを開始')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='セーフモード: 他のClaude Codeセッションを終了せずに新しいセッションを開始')
    parser.add_argument('--setup', action='store_true',
                       help='初期設定モード: 環境変数や設定ファイルを作成')
    parser.add_argument('--force-setup', action='store_true',
                       help='強制セットアップ: 既存のCLAUDE.mdを強制上書きしてbase-CLAUDE.mdから再作成')
    parser.add_argument('args', nargs='*', help='Claude Codeに渡す追加引数')
    
    args = parser.parse_args()
    
    # 初期設定モード
    if args.setup:
        print("🔧 初期設定モード")
        print("以下の環境変数を設定してください:")
        print(f"export CLAUDE_LOGIN_SCRIPT='{Path.home() / 'claude-login.py'}'")
        print(f"export CLAUDE_VENV_PATH='{Path.home() / 'venv'}'")
        print("")
        print("設定例 (~/.bashrc または ~/.zshrc に追加):")
        print("# Claude Code 自動化システム設定")
        print(f"export CLAUDE_LOGIN_SCRIPT='{Path.home() / 'claude-login.py'}'")
        print(f"export CLAUDE_VENV_PATH='{Path.home() / 'venv'}'")
        return
    
    # デフォルトは並列モード（--no-parallelが指定されていない場合）
    parallel_mode = not args.no_parallel
    skip_cleanup = args.no_cleanup or not args.no_parallel  # 並列モードまたは--no-cleanupでクリーンアップスキップ
    force_setup = getattr(args, 'force_setup', False)  # --force-setupオプション
    
    system = ClaudeCompleteSystem()
    success = system.run(args.project_type, args.args, parallel_mode, skip_cleanup, force_setup)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()