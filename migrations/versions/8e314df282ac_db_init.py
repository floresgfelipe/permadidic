"""DB init

Revision ID: 8e314df282ac
Revises: 
Create Date: 2022-08-11 10:51:53.663143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e314df282ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('rol', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    op.create_table('alumno',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('matricula', sa.String(length=10), nullable=True),
    sa.Column('nombres', sa.String(length=50), nullable=False),
    sa.Column('apellido_p', sa.String(length=50), nullable=False),
    sa.Column('apellido_m', sa.String(length=50), nullable=False),
    sa.Column('dia_nac', sa.Integer(), nullable=False),
    sa.Column('mes_nac', sa.String(length=20), nullable=False),
    sa.Column('año_nac', sa.Integer(), nullable=False),
    sa.Column('decanato', sa.String(length=50), nullable=False),
    sa.Column('parroquia', sa.String(length=80), nullable=False),
    sa.Column('telefono', sa.String(length=10), nullable=False),
    sa.Column('correo', sa.String(length=50), nullable=False),
    sa.Column('foto', sa.String(length=200), nullable=False),
    sa.Column('grado', sa.Integer(), nullable=False),
    sa.Column('grupo', sa.String(length=1), nullable=False),
    sa.Column('boleta_carta', sa.String(length=200), nullable=False),
    sa.Column('servicio', sa.String(length=2), nullable=False),
    sa.Column('calificacion1', sa.Integer(), nullable=True),
    sa.Column('calificacion2', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_soporte',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=200), nullable=True),
    sa.Column('decanato', sa.String(length=50), nullable=True),
    sa.Column('parroquia', sa.String(length=80), nullable=True),
    sa.Column('telefono', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('asunto', sa.Integer(), nullable=True),
    sa.Column('comentario', sa.Text(), nullable=True),
    sa.Column('resuelto', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket_soporte')
    op.drop_table('alumno')
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
