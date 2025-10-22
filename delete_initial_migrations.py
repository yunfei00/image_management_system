import os
import re
import sys


def find_initial_migrations(root_dir):
    """
    遍历项目根目录，查找所有符合条件的 0001_initial 迁移文件
    :param root_dir: 项目根目录（包含 manage.py 的目录）
    :return: 符合条件的文件路径列表
    """
    initial_files = []
    # 匹配 0001_initial.py 或 0001_initial.pyc 格式的文件
    pattern = re.compile(r'^00\d{2}.*\.py[co]?$')  # 包含 .py、.pyc、.pyo

    # 遍历项目根目录下的所有文件夹
    for dirpath, _, filenames in os.walk(root_dir):
        # 只处理 migrations 目录
        if os.path.basename(dirpath) == 'migrations':
            for filename in filenames:
                if 'venv' in dirpath:
                    continue
                if pattern.match(filename):
                    # 排除 __init__.py（虽然命名不匹配，但双重保险）
                    if filename == '__init__.py':
                        continue
                    file_path = os.path.join(dirpath, filename)
                    initial_files.append(file_path)
    return initial_files


def delete_files(file_list):
    """
    提示用户并删除指定文件列表
    :param file_list: 要删除的文件路径列表
    """
    if not file_list:
        print("未找到符合条件的 0001_initial 迁移文件。")
        return

    # 显示找到的文件
    print("找到以下文件，准备删除：")
    for i, file_path in enumerate(file_list, 1):
        print(f"{i}. {file_path}")

    # 确认删除
    confirm = input("\n确定要删除这些文件吗？(y/N) ").strip().lower()
    if confirm != 'y':
        print("已取消删除。")
        return

    # 执行删除
    deleted = 0
    failed = 0
    for file_path in file_list:
        try:
            os.remove(file_path)
            print(f"已删除：{file_path}")
            deleted += 1
        except Exception as e:
            print(f"删除失败 {file_path}：{str(e)}")
            failed += 1

    print(f"\n删除完成：成功 {deleted} 个，失败 {failed} 个。")


if __name__ == "__main__":
    # 获取项目根目录（默认当前目录，可通过命令行参数指定）
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()

    # 验证目录是否存在
    if not os.path.isdir(project_root):
        print(f"错误：目录不存在 - {project_root}")
        sys.exit(1)

    # 查找并删除文件
    initial_files = find_initial_migrations(project_root)
    delete_files(initial_files)