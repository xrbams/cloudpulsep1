const { createTeam, getTeams } = require('./teams');
const { createPlayer, getPlayers } = require('./players');

async function init() {
  // Create initial teams
  await createTeam('t-123-cbd', new Date(1980, 6, 20), 'Tampere', 'nike', 1);
  await createTeam('t-456-cbd', new Date(1980, 6, 21), 'Helsinki', 'adidas', 2);

  // Create initial players
  await createPlayer(1, 'Donkey', 'Kong', 10, 'Finnish', 170, 20, 'GoalKeeper');
  await createPlayer(2, 'Mario', 'Bros', 30, 'Italian', 150, 70, 'Forward');
  await createPlayer(3, 'Luigi', 'Bros', 28, 'Italian', 160, 65, 'Midfielder');
  await createPlayer(4, 'Peach', 'Princess', 25, 'Mushroom', 155, 50, 'Defender');

  // Fetch and log teams
  const teams = await getTeams();
  console.log('Teams:', teams);

  // Fetch and log players
  const players = await getPlayers();
  console.log('Players:', players);
}

init().catch(err => console.error(err));
