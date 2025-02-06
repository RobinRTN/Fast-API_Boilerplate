from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.sql import func
from typing import List, Optional

Base = declarative_base()

# Many-to-Many relationships
channel_brand = Table(
    "channel_brand",
    Base.metadata,
    Column("channel_id", Integer, ForeignKey("channels.id"), primary_key=True),
    Column("brand_id", Integer, ForeignKey("brands.id"), primary_key=True),
)

channel_size = Table(
    "channel_size",
    Base.metadata,
    Column("channel_id", Integer, ForeignKey("channels.id"), primary_key=True),
    Column("size_id", Integer, ForeignKey("sizes.id"), primary_key=True),
)

# ✅ User Model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))  # OAuth users may not have passwords
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship with channels
    channels: Mapped[List["Channel"]] = relationship(
        "Channel", back_populates="user", cascade="all, delete"
    )

# ✅ Brand Model
class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    channels: Mapped[List["Channel"]] = relationship(
        "Channel", secondary=channel_brand, back_populates="brands"
    )

# ✅ Size Model
class Size(Base):
    __tablename__ = "sizes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    channels: Mapped[List["Channel"]] = relationship(
        "Channel", secondary=channel_size, back_populates="sizes"
    )

# ✅ MainCategory & SubCategory Models
class MainCategory(Base):
    __tablename__ = "main_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)  # boys, girls, unisex

    subcategories: Mapped[List["SubCategory"]] = relationship(
        "SubCategory", back_populates="main_category"
    )

class SubCategory(Base):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)  # boys, girls, unisex
    main_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("main_categories.id"), nullable=False)

    main_category: Mapped["MainCategory"] = relationship("MainCategory", back_populates="subcategories")

# ✅ Channel Model
class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    query_identifier: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)  # Identifier for frontend params
    search: Mapped[Optional[str]] = mapped_column(String)  # Optional search query
    min_price: Mapped[Optional[int]] = mapped_column(Integer)  # Optional min price
    max_price: Mapped[Optional[int]] = mapped_column(Integer)  # Optional max price

    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    user: Mapped[Optional["User"]] = relationship("User", back_populates="channels", lazy="joined")

    sizes: Mapped[List["Size"]] = relationship(
        "Size", secondary=channel_size, back_populates="channels"
    )
    brands: Mapped[List["Brand"]] = relationship(
        "Brand", secondary=channel_brand, back_populates="channels"
    )

    main_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("main_categories.id"), index=True)
    main_category: Mapped[Optional["MainCategory"]] = relationship("MainCategory", back_populates="channels")

    sub_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subcategories.id"), index=True)
    sub_category: Mapped[Optional["SubCategory"]] = relationship("SubCategory", back_populates="channels")
