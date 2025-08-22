import os
import uuid

from fastapi import HTTPException, UploadFile

from app.configs import config

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]


async def upload_file(file: UploadFile, upload_dir: str) -> str:
    """
    입력받은 파일로부터 파일의 이름과 확장자를 분리하여 각각 변수에 담습니다.
    이후 파일이름에 uuid4의 hex 값을 추가하여 유니크한 파일 이름을 생성한 뒤 파일이름과 확장자를 다시 합쳐 변수에 담습니다.

    config에 설정된 MEDIA_DIR 경로와 파라미터로 입력받은 upload_dir 을 합쳐 파일을 저장할 디렉터리의 경로를 변수에 담습니다.
    만약 해당 경로에 디렉터리가 존재하지 않으면 생성합니다.

    위에서 지정한 유니크한 파일이름을 담은 변수, 파일을 저장할 디렉터리 경로 변수를 사용하여 파일을 업로드합니다.
    이후에 저장된 파일의 url을 리턴값으로 반환합니다.
    파일의 url은 upload_dir 과 파일이름을 포함하는 형태로 구성합니다.
    """
    # 파일 확장자 분리
    if file.filename and "." in file.filename:
        filename, ext = file.filename.rsplit(".", 1)
    else:
        filename = file.filename or "unknown"
        ext = ""

    # UUID가 추가된 유니크한 파일명 생성
    unique_filename = (
        f"{filename}_{uuid.uuid4().hex}.{ext}"
        if ext
        else f"{filename}_{uuid.uuid4().hex}"
    )

    upload_dir_path = os.path.join(config.MEDIA_DIR, upload_dir)
    os.makedirs(upload_dir_path, exist_ok=True)  # 업로드 폴더가 없으면 생성

    file_path = f"{upload_dir}/{unique_filename}"

    with open(f"{upload_dir_path}/{unique_filename}", "wb") as f:
        content = await file.read()
        f.write(content)

    return file_path


def delete_file(file_url: str) -> None:
    """
    파라미터로 입력받은 파일 url 으로부터 파일의 전체 경로를 생성하고
    해당 경로에 파일이 존재하는지 확인한 후, 파일이 존재한다면 해당파일을 삭제합니다.
    """
    file_path = f"{config.MEDIA_DIR}/{file_url}"

    if not os.path.exists(file_path):
        return

    os.remove(file_path)


def validate_image_extension(file: UploadFile) -> str:
    """
    입력받은 파일 객체의 확장자가 이미지 확장자인지 확인하는 함수입니다.

    입력받은 파일객체에서 파일명과 확장자를 분리합니다.
    확장자가 위에 선언된 IMAGE_EXTENSIONS 에 포함되는지 확인하고,
    만약 포함되어있지 않으면 HTTPException 예외를 발생시킵니다.

    확장자가 유효하면 확장자를 그대로 리턴합니다.
    """
    if file.filename and "." in file.filename:
        filename, ext = file.filename.rsplit(".", 1)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"invalid image extension. enable extension: {IMAGE_EXTENSIONS}",
        )

    if ext.lower() not in IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"invalid image extension. enable extension: {IMAGE_EXTENSIONS}",
        )
    return ext
