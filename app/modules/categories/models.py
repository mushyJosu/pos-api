from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("owner_id", "name", name="uq_category_owner_name"),)
    #UniqueConstraint prevents duplicate category names for the same user.
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(100))