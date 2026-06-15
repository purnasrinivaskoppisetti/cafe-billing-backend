from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    devices = relationship(
        "Device",
        back_populates="shop",
        cascade="all, delete-orphan"
    )


class Device(Base):
    __tablename__ = "devices"

    id = Column(
        String,
        primary_key=True
    )

    shop_id = Column(
        String,
        ForeignKey("shops.id", ondelete="CASCADE")
    )

    device_name = Column(
        String,
        nullable=False
    )

    shop = relationship(
        "Shop",
        back_populates="devices"
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    category_id = Column(
        String,
        ForeignKey("categories.id", ondelete="CASCADE")
    )

    category = relationship(
        "Category"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        String,
        primary_key=True
    )

    bill_number = Column(
        String,
        nullable=False
    )

    total_items = Column(
        Integer,
        nullable=False
    )

    sub_total = Column(
        Float,
        nullable=False
    )

    discount = Column(
        Float,
        nullable=False,
        default=0
    )

    grand_total = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True)
    )

    synced_at = Column(
        DateTime(timezone=True)
    )

    # No Foreign Key
    device_id = Column(
        String,
        nullable=True
    )

    items = relationship(
        "TransactionItem",
        back_populates="transaction",
        cascade="all, delete-orphan"
    )


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    transaction_id = Column(
        String,
        ForeignKey(
            "transactions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    product_id = Column(
        String
    )

    name = Column(
        String,
        nullable=False
    )

    rate = Column(
        Float,
        nullable=False
    )

    qty = Column(
        Integer,
        nullable=False
    )

    transaction = relationship(
        "Transaction",
        back_populates="items"
    )


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    transaction_id = Column(
        String,
        nullable=False
    )

    device_id = Column(
        String,
        nullable=False
    )

    synced_at = Column(
        DateTime(timezone=True)
    )