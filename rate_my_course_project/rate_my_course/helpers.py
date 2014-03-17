__author__ = 'liamfurphy'

def build_course_list_for_api(courses):
    results = []
    for r in courses:
        o = {
            "course_id": r.id,
            "average_satisfaction": float(r.average_satisfaction if r.average_satisfaction else 0),
            "average_difficulty": float(r.average_difficulty if r.average_difficulty else 0),
            "average_materials": float(r.average_materials if r.average_materials else 0),
            "course_name": r.course_name,
            "description": r.description,
            "lecturer": r.lecturer.name,
            "average_teaching": float(r.average_teaching if r.average_teaching else 0),
            "number_of_ratings": r.number_of_ratings,
            "average_overall": float(r.average_overall if r.average_overall else 0),
            "uni": r.uni.name,
            "course_code": r.course_code,
            "year_of_degree": r.year_of_degree,
            "uni_id": r.uni.id}
        results.append(o)
    return results
