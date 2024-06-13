const { bigQueryClient, datasetId } = require('./database');

const tableId = 'teams';

async function createTeam(team_name, date_of_issue, city, sponsor, playerId) {
  const query = `
    INSERT INTO \`${datasetId}.${tableId}\` (team_name, date_of_issue, city, sponsor, playerId)
    VALUES (@team_name, @date_of_issue, @city, @sponsor, @playerId)
  `;
  const options = {
    query: query,
    params: { team_name, date_of_issue, city, sponsor, playerId },
  };

  await bigQueryClient.query(options);
  console.log(`Team ${team_name} created successfully.`);
}

async function getTeams() {
  const query = `SELECT * FROM \`${datasetId}.${tableId}\``;
  const [rows] = await bigQueryClient.query(query);
  return rows;
}

module.exports = {
  createTeam,
  getTeams
};


