#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""higher_view_menu_name_length

Revision ID: e2e33bb26430
Revises: 952da73b5eff
Create Date: 2020-06-04 01:02:24.927468

"""

# revision identifiers, used by Alembic.
revision = "e2e33bb26430"
down_revision = "952da73b5eff"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "ab_view_menu",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=300),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "ab_view_menu",
        "name",
        existing_type=sa.VARCHAR(length=300),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
