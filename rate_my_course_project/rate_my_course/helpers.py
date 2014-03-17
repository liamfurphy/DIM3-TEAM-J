__author__ = 'liamfurphy'

def build_course_list_for_api(courses):
    results = []
    for r in courses:
        o = {
            "course_id": r.id,
            "average_satisfaction": r.average_satisfaction,
            "average_difficulty": r.average_difficulty,
            "average_materials": r.average_materials,
            "course_name": r.course_name,
            "description": r.description,
            "lecturer": r.lecturer.name,
            "average_teaching": r.average_teaching,
            "number_of_ratings": r.number_of_ratings,
            "average_overall": r.average_overall,
            "uni": r.uni.name,
            "course_code": r.course_code,
            "year_of_degree": r.year_of_degree,
            "uni_id": r.uni.id}
        results.append(o)
    return results
