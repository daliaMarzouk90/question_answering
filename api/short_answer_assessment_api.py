from flask import request, jsonify, Blueprint, make_response, abort
from controller.model_controller import ShortAnswersAssement

answer_assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')
answers_ass_controller = ShortAnswersAssement()

@answer_assessment_bp.route('/train', methods=['GET'])
def train_model():
    try:
        result = answers_ass_controller.train()
    except Exception as e:
        abort(make_response(jsonify(message=e.__str__()), 500,
                            {'Content-Type': 'application/json'}))
    
    return make_response(jsonify(status=True, progress=result), 201,
                                 {'Content-Type': 'application/json'})

@answer_assessment_bp.route('/test', methods=['GET'])
def test_model():
    try:
        result = answers_ass_controller.test()
    except Exception as e:
        abort(make_response(jsonify(message=e.__str__()), 500,
                            {'Content-Type': 'application/json'}))
    
    return make_response(jsonify(status=True, progress=result), 201,
                                 {'Content-Type': 'application/json'})

@answer_assessment_bp.route('/assess', methods=['POST'])
def assess():
    request_json_data = request.get_json()

    if("ReferenceAnswers" not in request_json_data or "Answer" not in request_json_data):
        abort(make_response(jsonify(message="assessment info no complete"), 503,
                            {'Content-Type': 'application/json'}))

    if (not isinstance(request_json_data["ReferenceAnswers"], list)):
        abort(make_response(jsonify(message="assessment answers should be a list"), 400,
                            {'Content-Type': 'application/json'}))

    if (not isinstance(request_json_data["Answer"], str)):
        abort(make_response(jsonify(message="the answer should be a string"), 400,
                            {'Content-Type': 'application/json'}))

    try:
        assesment = answers_ass_controller.assess(request_json_data["ReferenceAnswers"], request_json_data["Answer"])
    except Exception as e:
        abort(make_response(jsonify(message=e.__str__()), 500,
                            {'Content-Type': 'application/json'}))

    return make_response(jsonify(status=True, assesment=assesment), 200,
                                 {'Content-Type': 'application/json'})
