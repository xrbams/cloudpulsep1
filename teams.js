const { Model, DataTypes } = require("sequelize");

const sequelize = require("./database");

class Teams extends Model {}

Teams.init({
    // Model attributes (table columns) are defined here
    team_name: {
      type: DataTypes.STRING,
      primaryKey: true,
      allowNull: false, // as it appears in database
      defaultValue: 't-123-cbd',
    },
    date_of_issue: {
      type: DataTypes.DATE,  
      defaultValue: new Date(1980, 6, 20),
      allowNull: false,
    },
    city: {
        type: DataTypes.STRING,   
        defaultValue: "Tampere", 
        allowNull: false,
    },
    sponsor: {
        type: DataTypes.STRING,     //table, field, gym, 
        defaultValue: "nike",
        allowNull: false,
    }, 
    playerId: {
      type: DataTypes.INTEGER,
      allowNull: false,
    }
      
}, {
    sequelize,   // pass the connection instance
    tableName: "Teams",         // In database

    // Fields createdAt and updatedAt (DataTypes.DATE) would be
    // added automatically to model
    timestamps: false
});




module.exports = Teams;

