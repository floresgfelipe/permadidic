"""db init

Revision ID: e30adf7ddb74
Revises: 
Create Date: 2022-08-03 13:15:48.837401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e30adf7ddb74'
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
    sa.Column('nombres', sa.String(length=50), nullable=True),
    sa.Column('apellido_p', sa.String(length=50), nullable=True),
    sa.Column('apellido_m', sa.String(length=50), nullable=True),
    sa.Column('decanato', sa.String(length=50), nullable=True),
    sa.Column('parroquia', sa.String(length=80), nullable=True),
    sa.Column('telefono', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('foto', sa.String(length=120), nullable=True),
    sa.Column('grado', sa.Integer(), nullable=True),
    sa.Column('grupo', sa.String(length=1), nullable=True),
    sa.Column('pago', sa.Integer(), nullable=True),
    sa.Column('boleta', sa.String(length=120), nullable=True),
    sa.Column('servicio', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alumno_email'), 'alumno', ['email'], unique=True)
    op.create_table('evaluacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=True),
    sa.Column('descripcion', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('calificaciones',
    sa.Column('id_alumno', sa.Integer(), nullable=False),
    sa.Column('id_evaluacion', sa.Integer(), nullable=False),
    sa.Column('valor', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_alumno'], ['alumno.id'], ),
    sa.ForeignKeyConstraint(['id_evaluacion'], ['evaluacion.id'], ),
    sa.PrimaryKeyConstraint('id_alumno', 'id_evaluacion')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calificaciones')
    op.drop_table('evaluacion')
    op.drop_index(op.f('ix_alumno_email'), table_name='alumno')
    op.drop_table('alumno')
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###