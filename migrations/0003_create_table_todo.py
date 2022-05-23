"""
create table todo
date created: 2022-05-22 04:48:04.157648
"""

import datetime

def upgrade(migrator):
    migrator.drop_table('todo')
    with migrator.create_table('todo') as table:
        table.primary_key('id')
        table.char('desc', max_length=255)
        table.bool('done', default=False)
        table.int(
                'priority',
                choices=[(1, "High"), (2, "Medium"), (3, "Low")],
                default=2
            )
        table.char('blocked_reason', default='', max_length=255)
        table.datetime('created_date', default=datetime.datetime.now)
        table.datetime('updated_date', default=datetime.datetime.now)


def downgrade(migrator):
    migrator.drop_table('todo')
