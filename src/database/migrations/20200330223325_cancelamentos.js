
exports.up = function(knex) {
    return knex.schema.createTable('cancelamentos', function(table) {
        table.increments('id');
        table.string('user').notNullable();
        table.string('app');
        table.integer('time');
    });
};

exports.down = function(knex) {
  return knex.schema.dropTable('cancelamentos')
};
