import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("auto-memo")


@mcp.tool()
def memo_write(file_path: str, content: str, encoding: str = "utf-8") -> str:
    """指定ファイルにメモを追記する（UTF-8固定）"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding=encoding) as f:
        f.write(content)
    return f"書き込み完了: {file_path}"


@mcp.tool()
def memo_grep(file_path: str, keyword: str) -> list[dict]:
    """メモファイル内でキーワードを検索して重複チェック用に返す"""
    path = Path(file_path)
    if not path.exists():
        return []
    results = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if re.search(keyword, line):
                results.append({"line": i, "text": line.rstrip("\n")})
    return results


@mcp.tool()
def memo_read_last(file_path: str, lines: int = 10) -> str:
    """ファイルの末尾N行を取得する（追記前の確認用）"""
    path = Path(file_path)
    if not path.exists():
        return ""
    with path.open("r", encoding="utf-8") as f:
        all_lines = f.readlines()
    return "".join(all_lines[-lines:])


@mcp.tool()
def memo_write_both(
    memo_path: str,
    log_path: str,
    memo_content: str,
    log_line: str,
) -> dict:
    """01_memo.md と 00_mis_log.md に同時書き込みする（/memo-all 用）"""
    for file_path, content in [(memo_path, memo_content), (log_path, log_line)]:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(content)
    return {
        "memo": f"書き込み完了: {memo_path}",
        "log": f"書き込み完了: {log_path}",
    }


@mcp.tool()
def memo_read_context(
    log_path: str,
    config_path: str,
    index_path: str = "",
    log_lines: int = 10,
) -> dict:
    """mis_log末尾 と last_config.json を1回で取得する（/memo-all 用）"""
    import json

    log = Path(log_path)
    log_tail = ""
    if log.exists():
        with log.open("r", encoding="utf-8") as f:
            all_lines = f.readlines()
        log_tail = "".join(all_lines[-log_lines:])

    config = Path(config_path)
    config_data = {}
    if config.exists():
        with config.open("r", encoding="utf-8") as f:
            config_data = json.load(f)

    index = Path(index_path) if index_path else None
    index_text = ""
    if index and index.exists():
        with index.open("r", encoding="utf-8") as f:
            index_text = f.read()

    return {"log_tail": log_tail, "config": config_data, "index": index_text}


@mcp.tool()
def memo_write_all(
    memo_path: str,
    log_path: str,
    index_path: str,
    config_path: str,
    memo_content: str,
    log_content: str,
    index_line: str,
    new_last_line: int,
    last_submit_dir: str = "",
    highlight_line: str = "",
) -> dict:
    """01_memo.md・00_mis_log.md・インデックス・last_config を1回で書き込む（/memo-all 用）"""
    import json

    writes = [
        (memo_path, memo_content),
        (log_path, log_content),
        (index_path, index_line),
    ]
    for file_path, content in writes:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(content)

    config_path_obj = Path(config_path)
    config_path_obj.parent.mkdir(parents=True, exist_ok=True)
    with config_path_obj.open("w", encoding="utf-8") as f:
        json.dump(
            {"last_submit_dir": last_submit_dir, "last_memo_line": new_last_line},
            f,
            ensure_ascii=False,
            indent=2,
        )

    return {
        "memo": f"書き込み完了: {memo_path}",
        "log": f"書き込み完了: {log_path}",
        "index": f"書き込み完了: {index_path}",
        "config": f"更新完了: {config_path} (last_memo_line={new_last_line})",
        "highlight_line": highlight_line,
    }


if __name__ == "__main__":
    mcp.run()
