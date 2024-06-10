const { Model, DataTypes } = require("sequelize");

const sequelize = require("./database");


class Players extends Model {}

Players.init({
    // Model attributes (table columns) are defined here
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      allowNull: false,
      autoIncrement: false,
    },
    first_name: {
      type: DataTypes.STRING,   
      defaultValue: "donkey",
      allowNull: false,
    },
    last_name: {
        type: DataTypes.STRING,  
        defaultValue: "kong", 
        allowNull: false,
    },
    age: {
        type: DataTypes.INTEGER,    
        defaultValue: 10,
        allowNull: false,
    },
    nationality: {
        type: DataTypes.STRING,   
        defaultValue: "Finnish", 
        allowNull: false,
    },
    height: {
        type: DataTypes.INTEGER,    
        defaultValue: 170,
        allowNull: false,
    },
    weight: {
        type: DataTypes.INTEGER,    
        defaultValue: 20,
        allowNull: false,
    },
    position: {
        type: DataTypes.STRING,   
        defaultValue: "GoalKeeper", 
        allowNull: false,
    },
      
}, {
    sequelize,   // pass the connection instance
    tableName: "Players",         // In database


    // Fields createdAt and updatedAt (DataTypes.DATE) would be
    // added automatically to model
    timestamps: false
});



module.exports = Players;


