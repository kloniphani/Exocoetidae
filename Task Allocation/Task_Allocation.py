from Roommates.StableRoommates import *;

firstList = [{"name":'A',"age":40,"preferences":['U','V','W','X','Y','Z']},
                 {"name":'B',"age":21,"preferences":['V','W','Y','U','X','Z']},
                 {"name":'C',"age":30,"preferences":['V','W','U','Y','X','Z']},
                 {"name":'D',"age":50,"preferences":['V','W','U','Y','X','Z']},
                 {"name":'E',"age":28,"preferences":['U','W','V','Y','X','Z']},
                 {"name":'F',"age":28,"preferences":['V','W','U','Y','X','Z']}
            ]

secondList = [{"name":'U',"age":30,"preferences":['A','B','C','D','E','F']},
                 {"name":'V',"age":31,"preferences":['A','C','B','D','E','F']},
                 {"name":'W',"age":40,"preferences":['A','C','B','D','E','F']},
                 {"name":'X',"age":34,"preferences":['A','B','C','D','E','F']},
                 {"name":'Y',"age":45,"preferences":['A','B','C','D','E','F']},
                 {"name":'Z',"age":45,"preferences":['A','B','C','D','F','E']}
                ]


pg = StableRoommates(firstList, secondList)