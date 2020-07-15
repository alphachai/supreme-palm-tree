"""init

Revision ID: 4dfa4a93d27f
Revises: 
Create Date: 2020-07-15 16:14:58.288832

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4dfa4a93d27f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "topping",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_topping_id"), "topping", ["id"], unique=False)
    op.create_index(op.f("ix_topping_name"), "topping", ["name"], unique=True)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_id"), "order", ["id"], unique=False)
    op.create_table(
        "pizza",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["order.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pizza_id"), "pizza", ["id"], unique=False)
    op.create_table(
        "pizza_topping",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pizza_id", sa.Integer(), nullable=True),
        sa.Column("topping_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["pizza_id"], ["pizza.id"],),
        sa.ForeignKeyConstraint(["topping_id"], ["topping.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pizza_topping_id"), "pizza_topping", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_pizza_topping_id"), table_name="pizza_topping")
    op.drop_table("pizza_topping")
    op.drop_index(op.f("ix_pizza_id"), table_name="pizza")
    op.drop_table("pizza")
    op.drop_index(op.f("ix_order_id"), table_name="order")
    op.drop_table("order")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_topping_name"), table_name="topping")
    op.drop_index(op.f("ix_topping_id"), table_name="topping")
    op.drop_table("topping")
    # ### end Alembic commands ###
