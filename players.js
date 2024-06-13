const { bigQueryClient, datasetId } = require('./database');

const tableId = 'players';

async function createPlayer(id, first_name, last_name, age, nationality, height, weight, position) {
  const query = `
    INSERT INTO \`${datasetId}.${tableId}\` (id, first_name, last_name, age, nationality, height, weight, position)
    VALUES (@id, @first_name, @last_name, @age, @nationality, @height, @weight, @position)
  `;
  const options = {
    query: query,
    params: { id, first_name, last_name, age, nationality, height, weight, position },
  };

  await bigQueryClient.query(options);
  console.log(`Player ${first_name} ${last_name} created successfully.`);
}

async function getPlayers() {
  const query = `SELECT * FROM \`${datasetId}.${tableId}\``;
  const [rows] = await bigQueryClient.query(query);
  return rows;
}

module.exports = {
  createPlayer,
  getPlayers
};
