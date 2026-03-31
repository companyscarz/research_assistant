from flask import Blueprint, request, jsonify

#from research_assistant.src.research_assistant.main import kickoff
from research_assistant.src.research_assistant.main import research_on

#define blueprint
question_bp = Blueprint('question_bp', __name__)


#define route for blueprint
@question_bp.route('/user_query', methods=["POST"])
def Question():
    res = request.json
    user_query = res.get("user_query")

    try:
        search_results  = research_on(user_query)
        return jsonify({
            "research_results": search_results
            }), 200

    # except an error return error 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

    # close database finally
    finally:
        pass
