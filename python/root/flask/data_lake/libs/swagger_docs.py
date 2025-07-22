###########################################################################
#
#  Keep this up to date! https://www.youtube.com/watch?v=qztuEucrNBc
#
# https://swagger.io/docs/specification/v3_0/describing-parameters/
#
###########################################################################
swagger_dict = {
        'pets': {
        "parameters": [
            {
                "name": "userFirstName",
                "in": "header",
                "description": "Filter by first name. Partial Matches will be made.",
                "required": False,
                "type": "string",
            },
            {
                "name": "userLastName",
                "in": "header",
                "description": "Filter by last name.  Partial Matches will be made.",
                "required": False,
                "type": "string",
            },
            {
                "name": "tagPets",
                "in": "header",
                "description": """A JSON string representing a list of pet objects. Filters a list of records based on matching tag_name and/or tag_value pairs
                                    provided in the header. Supports partial matching (only tag_name or only tag_value) and lowercase. 
                                    Example: [{"tag_name":"Dog","tag_value":"Kumo"}]""",
                "required": False,
                "type": "string",
            },
            {
                "name": "page",
                "in": "header",
                "description": "Displays the records on the page number that was inputted. If left blank, defaults to displaying the first page. Must be a valid integer.",
                "required": False,
                "type": "int",
            },
            {
                "name": "segment",
                "in": "header",
                "description": "Returns the data for the inputted segment. If left blank, displays a list of the available segments for this endpoint.",
                "required": False,
                "type": "string",
            },             
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },
        'grades': {
        "parameters": [
            {
                "name": "name",
                "in": "header",
                "description": "Filter by name. Partial Matches will be made.",
                "required": False,
                "type": "string",
            },
            {
                "name": "typeName",
                "in": "header",
                "description": "Filter by type.  Partial Matches will be made.",
                "required": False,
                "type": "string",
            },
            {
                "name": "limit",
                "in": "header",
                "description": "Limit the number of records returned for debugging.",
                "required": False,
                "type": "int",
            },
            {
                "name": "tagSections",
                "in": "header",
                "description": """A JSON string representing a list of section objects. Filters a list of records based on matching tag_name and/or tag_value pairs
                                    provided in the header. Supports partial matching (only tag_name or only tag_value) and lowercase. 
                                    Example: [{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
                "required": False,
                "type": "string",
            },
            {
                "name": "tagAssessments",
                "in": "header",
                "description": """A JSON string representing a list of assessment objects. Filters a list of records based on matching tag_name and/or tag_value pairs
                                    provided in the header. Supports partial matching (only tag_name or only tag_value) and lowercase.
                                    Example: [{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
                "required": False,
                "type": "string",
            },
            {
                "name": "page",
                "in": "header",
                "description": "Displays the records on the page number that was inputted. If left blank, defaults to displaying the first page. Must be a valid integer.",
                "required": False,
                "type": "int",
            },            
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },
    'courses': {
        "parameters": [
            {
                "name": "BrightSpacePrograms",
                "in": "header",
                "description": "Filter by the name of a Program. Example - 'Advanced Literacy Micro-Credentials'",
                "required": False,
                "type": "string",
            },
            {
                "name": "OrgUnitId",
                "in": "header",
                "description": "Filter by OrgUnitId",
                "required": False,
                "type": "int",
            },
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },
    'enrollments': {
        "parameters": [
            {
                "name": "Department",
                "in": "header",
                "description": "Filter by Department(s).  eg -  [\"Literacy Coaching\", \"K12 Leadership\"]",
                "required": False,
                "type": "JSON",
            },
            {
                "name": "sectionName",
                "in": "header",
                "description": "Filter by sectionName.  Partial Matches will be made",
                "required": False,
                "type": "string",
            },
            {
                "name": "courseId",
                "in": "header",
                "description": "Filter by courseId.  Must be exact and treated as a number (int). eg -  [117, 125]",
                "required": False,
                "type": "JSON",
            },            
            {
                "name": "UserId",
                "in": "header",
                "description": "Filter by UserId - This is the user's email address. Maps to userEmail column in genius_enrollments table.",
                "required": False,
                "type": "string",
            },
            {
                "name": "userName",
                "in": "header",
                "description": "Filter by userName. Maps to userName column in genius_enrollments table.",
                "required": False,
                "type": "string",
            },
            {
                "name": "limit",
                "in": "header",
                "description": "Limit the number of records returned for debugging.",
                "required": False,
                "type": "int",
            },
            {
                "name": "tagSections",
                "in": "header",
                "description": """A JSON string representing a list of tag objects. Filters a list of records based on matching tag_name and/or tag_value pairs
                                    provided in the tagFilters header. Supports partial matching (only tag_name or only tag_value) and lowercase.
                                    Example: [{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
                "required": False,
                "type": "string",
            },
            {
                "name": "page",
                "in": "header",
                "description": "Displays the records on the page number that was inputted. If left blank, defaults to displaying the first page. Must be a valid integer.",
                "required": False,
                "type": "int",
            },             
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },
        'sis_users': {
        "parameters": [
            {
                "name": "firstName",
                "in": "header",
                "description": "Filter by firstName. Partial Matches will be made.",
                "required": False,
                "type": "string",
            },
            {
                "name": "lastName",
                "in": "header",
                "description": "Filter by lastName.  Partial Matches will be made.",
                "required": False,
                "type": "string",
            },
            {
                "name": "email",
                "in": "header",
                "description": "Filter by email.  Partial Matches will be made. Maps to email column in genius_users table.",
                "required": False,
                "type": "string",
            },
            {
                "name": "userName",
                "in": "header",
                "description": "Filter by userName.  Partial Matches will be made. Maps to userName column in genius_users table.",
                "required": False,
                "type": "string",
            },            
            {
                "name": "anonymize",
                "in": "header",
                "description": "If set to true, converts email to a SHA-256 hash function.",
                "required": False,
                "type": "boolean",
            },
            {
                "name": "limit",
                "in": "header",
                "description": "Limit the number of records returned for debugging.",
                "required": False,
                "type": "int",
            },
            {
                "name": "page",
                "in": "header",
                "description": "Displays the records on the page number that was inputted. If left blank, defaults to displaying the first page. Must be a valid integer.",
                "required": False,
                "type": "int",
            },                         
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },
        'assessment_answers': {
        "parameters": [
            {
                "name": "tagSections",
                "in": "header",
                "description": """A JSON string representing a list of section objects. Filters a list of records based on matching tag_name and/or tag_value pairs
                                    provided in the header. Supports partial matching (only tag_name or only tag_value) and lowercase. 
                                    Example: [{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
                "required": False,
                "type": "string",
            },
            {
                "name": "tagAssessments",
                "in": "header",
                "description": """A JSON string representing a list of assessment objects. Filters a list of records based on matching tag_name and/or tag_value pairs
                                    provided in the header. Supports partial matching (only tag_name or only tag_value) and lowercase.
                                    Example: [{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
                "required": False,
                "type": "string",
            },
            {
                "name": "limit",
                "in": "header",
                "description": "Limit the number of records returned for debugging.",
                "required": False,
                "type": "int",
            },
            {
                "name": "page",
                "in": "header",
                "description": "Displays the records on the page number that was inputted. If left blank, defaults to displaying the first page. Must be a valid integer.",
                "required": False,
                "type": "int",
            },          
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },


    'nwri_Overview1': {
        "parameters": [
            {
                "name": "districtname",
                "in": "header",
                "description": "Filter by the name of a district. Example - 'districtName = MIAMI_DADE'",
                "required": False,
                "type": "string",
            },
            {
                "name": "SchoolName",
                "in": "header",
                "description": "Filter by the name of a school. Example - 'SchoolName = MIAMI_HIGH'",
                "required": False,
                "type": "string",
            },
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Welcome GeeksforGeeks!!"},
                            }
                        }
                    }
                },
            }
        },
    },



  'eligibleNotEnrolled': {
        "parameters": [
            {
                "name": "standardizeddistrict",
                "in": "header",
                "description": "Filter by standardized_district.",
                "required": False,
                "type": "string",
            },
            {
                "name": "schoolName",
                "in": "header",
                "description": "Filter by schoolName.",
                "required": False,
                "type": "string",
            },
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },
 

 
  'eligibleAndEnrolled': {
        "parameters": [
            {
                "name": "districtname",
                "in": "header",
                "description": "Filter by districtname.",
                "required": False,
                "type": "string",
            },
            {
                "name": "schoolName",
                "in": "header",
                "description": "Filter by schoolName.",
                "required": False,
                "type": "string",
            },
            # {
            #     "name": "page",
            #     "in": "header",
            #     "description": "Filter to fit to page.",
            #     "required": False,
            #     "type": "int",
            # },
           
        ],
        "responses": {
            200: {
                "description": "A status code 200 means successful and returns a message.",
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Successful response",
                                "value": {"message": "Request was successful."},
                            }
                        }
                    }
                },
            }
        },
    },

   

}

