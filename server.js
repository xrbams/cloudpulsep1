const { BigQuery } = require('@google-cloud/bigquery');

const bigQueryClient = new BigQuery();

exports.getPlayers = async (req, res) => {
  const query = `SELECT * FROM \`smart-charter-422809-k0.sports_data.players\` LIMIT 100`;
  const options = {
    query: query,
    location: 'US',
  };

  try {
    const [rows] = await bigQueryClient.query(options);
    res.status(200).json(rows);
  } catch (err) {
    console.error('ERROR:', err);
    res.status(500).send(err);
  }
};






// var express = require('express');
// const sequelize = require('./database');
// const Players = require('./players')
// const Teams = require('./teams')


// //foreign key association.
// Players.hasMany(Teams, { foreignKey: 'playerId' });
// Teams.belongsTo(Players, { foreignKey: 'playerId' });



// //{alter: true, force: true}
// sequelize.sync().then(() => {
//     console.log('database is ready');
//     //carInstance;
// }).catch((err) => {
//     console.log(err);
// });

// var app = express();

// app.use(express.json());

// var port = 8080;    // app.listen(8080);
// var HTTP_REQUEST_OK = 200;
// var HTTP_REQUEST_NOK = 404;
// var HTTP_REQUEST_NA = 405;



// //Players--------------------------------------------------------------------
// //get all
// app.get('/players', async (req, res) => {
//     try {
//         const player = await Players.findAll({ include: Teams });
//         res.status(HTTP_REQUEST_OK).send(player);
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NOK);
//     }

// })



// //get one based on Id
// app.get('/players/:id', async (req, res) => {
//     try {
//         const requestId = req.params.id;
//         const player = await Players.findByPk(requestId,
//             {
//                 include: Teams,
//             });
//         res.status(HTTP_REQUEST_OK).send(player);
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NOK);
//     }

// })



// //post one car
// app.post('/players', async (req, res) => {
//     try {
//         await Players.create(req.body);
//         res.status(HTTP_REQUEST_OK).send('Player is inserted ...');
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NOK);
//     }

// })



// //update a player team
// app.put('/players/:id/teams', async (req, res) => {
//     try {
//         const requestId = req.params.id;
//         const player = await Players.findOne({
//             where: { id: requestId },
//             include: Teams
//         });
//         const T = req.body;
//         const newTeam = await Teams.create(T);

//         await player.addTeam(newTeam);
//         await player.reload();

//         res.status(HTTP_REQUEST_OK).send(player);
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NA);
//     }

// })




// //Teams----------------------------------------------------------------------
// //get all 
// app.get('/teams', async (req, res) => {
//     try {
//         const team = await Teams.findAll({
//             include: Players
//         });
//         res.status(HTTP_REQUEST_OK).send(team);
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NOK);
//     }

// })



// //get one based on team name
// app.get('/teams/:team', async (req, res) => {
//     try {
//         const requestTeam = req.params.team;
//         const team = await Teams.findOne({ where: { team_name: requestTeam } });
//         res.status(HTTP_REQUEST_OK).send(team);
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NOK);
//     }

// })



// //post one plate at a time.
// app.post('/teams', async (req, res) => {
//     try {
//         await Teams.create(req.body)
//         res.status(HTTP_REQUEST_OK).send('Teams added ... ');
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NOK);
//     }

// })



// //update Teams. only city though
// app.put('/teams/:place', async (req, res) => {
//     try {
//         const requestP = req.params.place;
//         const place = await Teams.findOne({ where: { city: requestP } });
//         place.city = req.body.city;
//         await place.save();
//         res.status(HTTP_REQUEST_OK).send(place);
//     } catch (err) {
//         console.error(err);
//         res.status(HTTP_REQUEST_NA);
//     }
// })

// //-------------------------------------------------------------------------

// app.listen(port, () => {
//     console.log(`Example server listening at http://localhost:${port}`)
// })