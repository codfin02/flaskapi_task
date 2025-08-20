import random
from typing import ClassVar, List, Optional, Union
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel:
    _data: ClassVar[List["UserModel"]] = []  # 전체 사용자 데이터를 저장하는 리스트
    _id_counter: ClassVar[int] = 1  # ID 자동 증가를 위한 카운터

    def __init__(self, username: str, password: str, age: int, gender: str) -> None:
        self.id = UserModel._id_counter
        self.username = username
        self.password = self.get_hashed_password(password)
        self.age = age
        self.gender = gender
        self.last_login = None

        # 클래스가 인스턴스화 될 때 _data에 추가하고 _id_counter를 증가시킴
        UserModel._data.append(self)
        UserModel._id_counter += 1

    @staticmethod
    def get_hashed_password(password: str) -> str:
        """비밀번호 해시화"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional["UserModel"]:
        """사용자 인증"""
        for user in cls._data:
            if user.username == username and cls.verify_password(password, user.password):
                return user
        return None

    @classmethod
    def create(cls, username: str, password: str, age: int, gender: str) -> "UserModel":
        """새로운 유저 추가"""
        return cls(username, password, age, gender)

    @classmethod
    def get(cls, **kwargs: Union[str, int]) -> Optional["UserModel"]:
        """단일 객체를 반환 (없으면 None)"""
        for user in cls._data:
            if all(getattr(user, key) == value for key, value in kwargs.items()):
                return user
        return None

    @classmethod
    def filter(cls, **kwargs: Union[str, int]) -> List["UserModel"]:
        """조건에 맞는 객체 리스트 반환"""
        return [
            user
            for user in cls._data
            if all(getattr(user, key) == value for key, value in kwargs.items())
        ]

    def update(self, **kwargs: Union[str, int, None]) -> None:
        """객체의 필드 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)

    def delete(self) -> None:
        """현재 인스턴스를 _data 리스트에서 삭제"""
        if self in UserModel._data:
            UserModel._data.remove(self)

    @classmethod
    def all(cls) -> List["UserModel"]:
        """모든 사용자 반환"""
        return cls._data

    @classmethod
    def create_dummy(cls) -> None:
        for i in range(1, 11):
            cls(
                username=f"dummy{i}",
                password=f"password{i}",
                age=15 + i,
                gender=random.choice(["male", "female"]),
            )

    @classmethod
    def clear(cls) -> None:
        """테스트를 위해 데이터를 초기화"""
        cls._data.clear()
        cls._id_counter = 1

    def __repr__(self) -> str:
        return f"UserModel(id={self.id}, username='{self.username}', age={self.age}, gender='{self.gender}')"

    def __str__(self) -> str:
        return self.username
