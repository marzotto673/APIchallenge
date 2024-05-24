const express = require('express');
const bodyParser = require('body-parser');
const { Sequelize, Model, DataTypes } = require('sequelize');

const app = express();
const port = 3000;

// Create Sequelize instance
const sequelize = new Sequelize({
    dialect: 'sqlite',
    storage: './database.sqlite'
});

// Define Rule model
class Rule extends Model {}

Rule.init({
    name: DataTypes.STRING,
    rule: DataTypes.STRING,
}, { sequelize, modelName: 'rule' });

// Sync models with database
sequelize.sync();

// Middleware for parsing request body
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// --

// Routes for Rule
app.get('/rules', async (req, res) => {
    const rules = await Rule.findAll();
    res.json(rules);
});

app.get('/rules/:id', async (req, res) => {
    const rule = await Rule.findByPk(req.params.id);

    if (rule) {
        return res.json(rule);
    }

    return res.status(404).send('Rule not found');
});

app.post('/rules', async (req, res) => {
    const rule = await Rule.create(req.body);
    res.json(rule);
});

// --

// Routes for Analyze text/file
app.post('/analyze/text', async (req, res) => {
    const { text, rules } = req.body;
    const ruleList = rules.map(({ rule_id }) => rule_id);

    const selectedRules = await Rule.findAll({
        where: {
            'id': {
                [Sequelize.Op.in]: ruleList,
            },
        },
    });

    res.send(selectedRules);
});

app.post('/analyze/file', () => {

});

// -- 

app.listen(port, () => {
    console.log(`api init on port ${port}`);
});
