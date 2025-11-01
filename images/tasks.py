# tasks.py
from celery import shared_task
import subprocess
import os


@shared_task
def push_image_to_registry(image_zip_path, project_slug, app_name, tag):
    """
    Celery 任务：将镜像从本地上传到 Docker Registry（localhost:5000），并获取 digest
    """
    # 工作目录路径
    workspace_dir = os.path.join('/data/app/media', project_slug, 'workspace')
    output_dir = os.path.join('/data/app/media', project_slug, 'output')

    # 创建目录（如果不存在）
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 解压上传的 image.zip
    subprocess.run(['Expand-Archive', '-Path', image_zip_path, '-DestinationPath', workspace_dir], check=True)

    # 假设解压后是 image.tar
    image_tar_path = os.path.join(workspace_dir, 'image.tar')

    if not os.path.exists(image_tar_path):
        raise FileNotFoundError(f"解压后的文件 {image_tar_path} 不存在。")

    # 使用 Docker 加载镜像
    subprocess.run(['docker', 'load', '-i', image_tar_path], check=True)

    # 重新打标签到本地 registry
    registry_url = "localhost:5000"
    full_tag = f"{registry_url}/{app_name}:{tag}"
    subprocess.run(['docker', 'tag', f"{app_name}:{tag}", full_tag], check=True)

    # 推送镜像
    subprocess.run(['docker', 'push', full_tag], check=True)

    # 获取镜像的 digest
    digest = subprocess.check_output(['docker', 'inspect', '--format', '{{index .RepoDigests 0}}', full_tag],
                                     text=True).strip()

    # 保存镜像的 digest
    digest_file_path = os.path.join(output_dir, 'image_digest.txt')
    with open(digest_file_path, 'w') as f:
        f.write(digest)

    # 返回 digest
    return digest
