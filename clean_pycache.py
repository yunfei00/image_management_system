import os
import shutil
import sys


def find_pycache_dirs(root_dir):
    """遍历根目录，查找所有__pycache__目录"""
    pycache_dirs = []
    for dirpath, dirnames, _ in os.walk(root_dir):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            pycache_dirs.append(pycache_path)
    return pycache_dirs


def delete_dirs(dirs):
    """删除指定的目录列表，返回删除成功和失败的数量"""
    success = 0
    failed = 0
    failed_dirs = []

    for dir_path in dirs:
        try:
            # 递归删除目录及其内容
            shutil.rmtree(dir_path)
            print(f"已删除：{dir_path}")
            success += 1
        except Exception as e:
            print(f"删除失败 {dir_path}：{str(e)}")
            failed += 1
            failed_dirs.append((dir_path, str(e)))

    return success, failed, failed_dirs


def main():
    # 获取用户指定的根目录（默认当前目录）
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.getcwd()

    # 验证目录是否存在
    if not os.path.isdir(root_dir):
        print(f"错误：目录不存在 - {root_dir}")
        sys.exit(1)

    # 查找所有__pycache__目录
    print(f"正在 {root_dir} 中查找__pycache__目录...")
    pycache_dirs = find_pycache_dirs(root_dir)

    if not pycache_dirs:
        print("未找到任何__pycache__目录。")
        return

    # 显示待删除目录
    print("\n找到以下__pycache__目录：")
    for i, dir_path in enumerate(pycache_dirs, 1):
        print(f"{i}. {dir_path}")

    # 确认删除
    confirm = input("\n确定要删除这些目录吗？(y/N) ").strip().lower()
    if confirm != "y":
        print("已取消删除。")
        return

    # 执行删除
    print("\n开始删除...")
    success, failed, failed_dirs = delete_dirs(pycache_dirs)

    # 输出结果
    print(f"\n处理完成：")
    print(f"成功删除 {success} 个__pycache__目录")
    if failed > 0:
        print(f"删除失败 {failed} 个目录（可能是权限问题）：")
        for dir_path, error in failed_dirs:
            print(f"  - {dir_path}：{error}")


if __name__ == "__main__":
    main()