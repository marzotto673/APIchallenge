from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import yara

# Configurações
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///challenge.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Rule model
class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rule = db.Column(db.String(120), nullable=False)

    def __getitem__(self, field):
        return self.__dict__[field]

# Cria todas as tabelas
with app.app_context(): 
    db.create_all()

# Rota padrão
@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'project': 'API Challenge',
        'author': 'Fernando Marzotto'
    })

# Rotas para rule
@app.route('/rules', methods=['GET'])
def get_rules():
    rules = Rule.query.all()
    return jsonify([{'id': rule.id, 'name': rule.name, 'rule': rule.rule} for rule in rules])

@app.route('/rules/<int:id>', methods=['GET'])
def get_rule(id):
    rule = Rule.query.get(id)
    if rule:
        return jsonify({'id': rule.id, 'name': rule.name, 'rule': rule.rule})
    return jsonify({'error': 'Rule not found'}), 404

@app.route('/rules', methods=['POST'])
def create_rule():
    data = request.get_json()
    new_rule = Rule(name=data['name'], rule=data['rule'])
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({'id': new_rule.id, 'name': new_rule.name, 'rule': new_rule.rule}), 201

# Rota para analyze text
@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    rule_ids = [rule['rule_id'] for rule in data['rules']]
    selected_rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    result = []

    for rule_item in selected_rules:
      rule = yara.compile(source=rule_item['rule'])
      matches = []
      for m in rule.match(data=data['text']):
        matches.append(m.rule)
      result.append(matches)
    return result

# Roda aplicação
if __name__ == '__main__':
    app.run(debug=True, port=8000)
