q9="""
Read the question that would be provided to you carefully.
It is about calculating total marks in a subject for students that have scored alteast some
marks in another subject AND are part of the required group. I want you to extract these.
I want you to return these details in a well structured json as your only output. Here is the format:
{
    "subject": "<Subject for which total marks has to be computed>",
    "filter_subject": "<Subject that acts as the filter>",
    "filter_score": "<The score required for 'filter_subject'>",
    "group": "<group range to which the students must belong>"
}

An example output would be,
{
    "subject": "Economics",
    "filter_subject": "English",
    "group": "51-90"
}
"""