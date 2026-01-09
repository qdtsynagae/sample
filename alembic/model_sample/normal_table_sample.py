"""Sample: pure SQLAlchemy table definition (for documentation)."""

import sqlalchemy as sa

example_table = sa.Table(
    "example_table",
    sa.MetaData(),
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(100), nullable=False),
)
