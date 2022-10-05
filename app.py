from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mad Libs templates
MAD_LIBS = [
    {
        "title": "A Day at the Zoo",
        "template": "Yesterday I went to the zoo with my {adjective1} {noun1}. We saw a {adjective2} {noun2} {verb1}ing on a {noun3}. The zookeeper told us it was {adjective3} to see such behavior. Then we ate {food} for lunch and {verb2}ed all afternoon.",
        "blanks": [
            {"prompt": "Adjective", "key": "adjective1"},
            {"prompt": "Noun", "key": "noun1"},
            {"prompt": "Adjective", "key": "adjective2"},
            {"prompt": "Noun", "key": "noun2"},
            {"prompt": "Verb (present tense)", "key": "verb1"},
            {"prompt": "Noun", "key": "noun3"},
            {"prompt": "Adjective", "key": "adjective3"},
            {"prompt": "Type of food", "key": "food"},
            {"prompt": "Verb (base form)", "key": "verb2"}
        ]
    },
    {
        "title": "Space Adventure",
        "template": "Captain {name} and the crew of the {adjective1} {noun1} were on a mission to {verb1} the {adjective2} {noun2}. Suddenly, their {noun3} detected a {adjective3} {noun4} approaching at {number} light years per hour! 'This is {exclamation}!' shouted the captain as they prepared to {verb2}.",
        "blanks": [
            {"prompt": "Name", "key": "name"},
            {"prompt": "Adjective", "key": "adjective1"},
            {"prompt": "Noun", "key": "noun1"},
            {"prompt": "Verb (base form)", "key": "verb1"},
            {"prompt": "Adjective", "key": "adjective2"},
            {"prompt": "Noun", "key": "noun2"},
            {"prompt": "Noun", "key": "noun3"},
            {"prompt": "Adjective", "key": "adjective3"},
            {"prompt": "Noun", "key": "noun4"},
            {"prompt": "Number", "key": "number"},
            {"prompt": "Exclamation", "key": "exclamation"},
            {"prompt": "Verb (base form)", "key": "verb2"}
        ]
    },
    {
        "title": "The Crazy Dream",
        "template": "Last night I had the {adjective1} dream. I was a {noun1} {verb1}ing in a {noun2} made of {food}. Suddenly, a {adjective2} {noun3} appeared and started {verb2}ing uncontrollably. 'This can't be real!' I shouted, but then I {verb3}ed and turned into a {adjective3} {noun4}. When I woke up, I was covered in {noun5}!",
        "blanks": [
            {"prompt": "Adjective", "key": "adjective1"},
            {"prompt": "Noun", "key": "noun1"},
            {"prompt": "Verb (present tense)", "key": "verb1"},
            {"prompt": "Noun", "key": "noun2"},
            {"prompt": "Type of food", "key": "food"},
            {"prompt": "Adjective", "key": "adjective2"},
            {"prompt": "Noun", "key": "noun3"},
            {"prompt": "Verb (present tense)", "key": "verb2"},
            {"prompt": "Verb (base form)", "key": "verb3"},
            {"prompt": "Adjective", "key": "adjective3"},
            {"prompt": "Noun", "key": "noun4"},
            {"prompt": "Noun (plural)", "key": "noun5"}
        ]
    }
]

@app.route('/')
def home():
    return render_template('madlibs.html')

@app.route('/get_stories', methods=['GET'])
def get_stories():
    # Return just the titles for the dropdown
    stories = [{"id": idx, "title": story["title"]} for idx, story in enumerate(MAD_LIBS)]
    return jsonify({"stories": stories})

@app.route('/get_story/<int:story_id>', methods=['GET'])
def get_story(story_id):
    if story_id < 0 or story_id >= len(MAD_LIBS):
        return jsonify({"error": "Invalid story ID"}), 400
    
    story = MAD_LIBS[story_id]
    return jsonify({
        "title": story["title"],
        "blanks": story["blanks"]
    })

@app.route('/generate_story/<int:story_id>', methods=['POST'])
def generate_story(story_id):
    if story_id < 0 or story_id >= len(MAD_LIBS):
        return jsonify({"error": "Invalid story ID"}), 400
    
    data = request.json
    story_template = MAD_LIBS[story_id]["template"]
    
    # Fill in the blanks
    try:
        filled_story = story_template.format(**data)
        return jsonify({
            "title": MAD_LIBS[story_id]["title"],
            "story": filled_story
        })
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)