from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, mapped_column, Mapped


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)